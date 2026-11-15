import os
import numpy as np
import pandas as pd
import pymannkendall as mk
from scipy import stats


MIN_OBSERVATIONS = 12


def compute_series_trend(
    df_series: pd.DataFrame,
    alpha: float = 0.05,
    min_obs: int = MIN_OBSERVATIONS,
) -> dict:
    """Compute OLS linear regression, Mann-Kendall test, and Sen's slope on a monthly series."""
    df_clean = df_series.sort_values("time").dropna(subset=["value"]).copy()
    n_total = len(df_series)
    n_valid = len(df_clean)

    first_row = df_series.iloc[0]
    base = {
        "basin_id": first_row["basin_id"],
        "basin_name": first_row["basin_name"],
        "region_type": first_row["region_type"],
        "variable_id": first_row["variable_id"],
        "time_start": str(df_series["time"].min().date()),
        "time_end": str(df_series["time"].max().date()),
        "temporal_resolution": "monthly",
        "n_observations": n_valid,
        "alpha": alpha,
        "method": "Mann-Kendall + Sen's Slope + OLS",
        "data_coverage": round(n_valid / n_total, 4) if n_total > 0 else 0.0,
    }

    units = first_row["units"]
    slope_units = f"{units}/year"

    if n_valid < min_obs:
        return {
            **base,
            "slope": np.nan,
            "slope_units": slope_units,
            "sen_slope": np.nan,
            "p_value": np.nan,
            "trend_direction": "undetermined",
            "significance": "insufficient_data",
            "notes": f"Only {n_valid} valid observations (< {min_obs} required).",
        }

    # Time in years since start for OLS slope in units/year
    t_years = (df_clean["time"] - df_clean["time"].iloc[0]).dt.days.to_numpy() / 365.25
    y = df_clean["value"].to_numpy(dtype=float)

    ols_res = stats.linregress(t_years, y)
    mk_res = mk.original_test(y, alpha=alpha)

    # mk.original_test returns Sen's slope per time step (1 month); multiply by 12 for per-year
    sen_slope_yr = float(mk_res.slope) * 12.0
    p_val = float(mk_res.p)

    if p_val < alpha:
        sig = "significant"
        direction = "increasing" if sen_slope_yr > 0 else ("decreasing" if sen_slope_yr < 0 else "no_detected_trend")
    else:
        sig = "not_significant"
        direction = "no_detected_trend"

    return {
        **base,
        "slope": float(ols_res.slope),
        "slope_units": slope_units,
        "sen_slope": sen_slope_yr,
        "p_value": p_val,
        "trend_direction": direction,
        "significance": sig,
        "notes": "Bounding-box area average; monthly data (seasonality not removed).",
    }


def run_trend_analysis(
    input_path: str = "data/processed/tabular/timeseries_all.parquet",
    output_path: str = "outputs/statistics/trend_results_all.csv",
) -> pd.DataFrame:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df = pd.read_parquet(input_path)

    results = []
    for (_, _), group in df.groupby(["basin_id", "variable_id"], sort=False):
        results.append(compute_series_trend(group))

    res_df = pd.DataFrame(results)
    res_df.to_csv(output_path, index=False)
    return res_df


if __name__ == "__main__":
    res = run_trend_analysis()
    print(f"Computed trends for {len(res)} series -> outputs/statistics/trend_results_all.csv")
    print(res[["basin_id", "basin_name", "variable_id", "sen_slope", "p_value", "trend_direction", "significance"]].to_string(index=False))
