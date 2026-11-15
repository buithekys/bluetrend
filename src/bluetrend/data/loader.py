import os
from datetime import datetime, timezone
import numpy as np
import pandas as pd


BASIN_REGISTRY = [
    ("basin_01", "Irrawaddy & Salween", "river_basin", "Luu vuc Song Irrawaddy & Salween.csv"),
    ("basin_02", "Kampar & Pahang", "river_basin", "Luu vuc song Kampar & Pahang.csv"),
    ("basin_03", "Kapuas & Mahakam", "river_basin", "Luu vuc song Kapuas & Mahakam.csv"),
    ("basin_04", "Mekong & Chao Phraya", "river_basin", "Luu vuc song Mekong & Chao Phraya.csv"),
    ("basin_05", "Thu Bon & Song Con", "river_basin", "Luu vuc Sông Thu Bồn & Sông Côn.csv"),
    ("basin_06", "Cagayan & Kinabatangan", "river_basin", "Song Cagayan & Kinabatangan.csv"),
    ("basin_07", "Hong - Thai Binh", "river_basin", "Song Hong-Thai Binh.csv"),
    ("marine_01", "Andaman Sea", "marine_region", "Bien Andaman.csv"),
    ("marine_02", "Sulawesi Sea", "marine_region", "Bien Sulawesi.csv"),
    ("marine_03", "Central Coast (Vietnam)", "marine_region", "Central Coast.csv"),
    ("marine_04", "Indonesian Archipelago", "marine_region", "Indonesian Archipelago.csv"),
    ("marine_05", "Strait of Malacca", "marine_region", "Strait of Malacca.csv"),
    ("marine_06", "Gulf of Thailand & SW Vietnam", "marine_region", "Vinh Thai Lan & Tay Nam Bo.csv"),
    ("marine_07", "Gulf of Tonkin (Vinh Bac Bo)", "marine_region", "VinhBacBo.csv"),
    ("region_sea", "Southeast Asia (Overview)", "regional_overview", "DongNamA.csv"),
]


def load_giovanni_csv(filepath: str, basin_id: str, basin_name: str, region_type: str) -> pd.DataFrame:
    """Load a NASA Giovanni area-averaged monthly CSV into canonical long format."""
    with open(filepath, "r", encoding="utf-8-sig") as fh:
        meta_lines = [fh.readline().strip() for _ in range(7)]

    fill_line = meta_lines[6]
    if "GPM" in fill_line:
        var_id = "precipitation"
        units = "mm/hr"
        product_name = "GPM_3IMERGM_07"
        fill_val = -9999.9
    elif "KD" in fill_line:
        var_id = "kd490"
        units = "m^-1"
        product_name = "MODISA_L3m_KD_Mo_4km_R2022_0"
        fill_val = -32767.0
    else:
        var_id = "unknown"
        units = "unknown"
        product_name = "unknown"
        fill_val = None

    df = pd.read_csv(filepath, skiprows=8)
    time_col, val_col = df.columns[0], df.columns[1]

    out = pd.DataFrame()
    out["basin_id"] = [basin_id] * len(df)
    out["basin_name"] = basin_name
    out["region_type"] = region_type
    out["time"] = pd.to_datetime(df[time_col])
    out["variable_id"] = var_id

    vals = pd.to_numeric(df[val_col], errors="coerce")
    if fill_val is not None:
        is_fill = np.isclose(vals, fill_val, rtol=1e-4, atol=1e-4)
        vals = vals.where(~is_fill, np.nan)
    out["value"] = vals
    out["units"] = units
    out["statistic"] = "area_mean"
    out["source_dataset_id"] = os.path.splitext(os.path.basename(filepath))[0]
    out["product_name"] = product_name
    out["quality_flag"] = np.where(out["value"].notna(), "pass", "missing_fill")
    return out


def build_normalized_timeseries(output_path: str = "data/processed/tabular/timeseries_all.parquet") -> pd.DataFrame:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    os.makedirs("metadata", exist_ok=True)

    frames = []
    for basin_id, basin_name, region_type, fname in BASIN_REGISTRY:
        fpath = os.path.join("data", "raw", "tabular", fname)
        if not os.path.exists(fpath):
            fpath = fname
        if os.path.exists(fpath):
            frames.append(load_giovanni_csv(fpath, basin_id, basin_name, region_type))

    combined = pd.concat(frames, ignore_index=True)
    combined.to_parquet(output_path, index=False)

    log_path = "metadata/processing_log.csv"
    log_entry = pd.DataFrame(
        [
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "step": "build_normalized_timeseries",
                "input_count": len(frames),
                "output_file": output_path,
                "n_rows": len(combined),
                "status": "success",
            }
        ]
    )
    if os.path.exists(log_path):
        log_entry.to_csv(log_path, mode="a", header=False, index=False)
    else:
        log_entry.to_csv(log_path, index=False)

    return combined


if __name__ == "__main__":
    df = build_normalized_timeseries()
    print(f"Saved {len(df)} normalized rows to data/processed/tabular/timeseries_all.parquet")
