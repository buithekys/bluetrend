import json
import os
import geopandas as gpd
import numpy as np
import pandas as pd
import pymannkendall as mk
import xarray as xr


def load_giovanni_2003_2024(filepath: str) -> dict:
    df = pd.read_csv(filepath, skiprows=8)
    df.columns = ["time", "value"]
    df["time"] = pd.to_datetime(df["time"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df[df["value"] > -100].dropna().sort_values("time")

    y = df["value"].to_numpy(dtype=float)
    mk_res = mk.original_test(y, alpha=0.05)
    sen_yr = float(mk_res.slope) * 12.0

    # Annual means for clean chart + 2025-2027 linear projection
    df["year"] = df["time"].dt.year
    annual = df.groupby("year")["value"].mean().reset_index()
    years = annual["year"].to_list()
    vals = [round(float(v), 4) for v in annual["value"].to_list()]

    last_val = vals[-1]
    proj_years = [2025, 2026, 2027]
    proj_vals = [round(last_val + sen_yr * (i + 1), 4) for i in range(3)]

    return {
        "n_months": len(df),
        "time_start": str(df["time"].min().date()),
        "time_end": str(df["time"].max().date()),
        "sen_slope_yr": round(sen_yr, 6),
        "p_value": round(float(mk_res.p), 6),
        "significant": bool(mk_res.p < 0.05),
        "annual_years": years,
        "annual_vals": vals,
        "proj_years": proj_years,
        "proj_vals": proj_vals,
    }


def sample_nc_at_points(nc_path: str, var_name: str, lons: np.ndarray, lats: np.ndarray) -> np.ndarray:
    ds = xr.open_dataset(nc_path)
    da = ds[var_name]
    vals = []
    for lon, lat in zip(lons, lats):
        try:
            v = float(da.sel(lon=lon, lat=lat, method="nearest").values)
            vals.append(v if np.isfinite(v) and v > -100 else np.nan)
        except Exception:
            vals.append(np.nan)
    ds.close()
    return np.array(vals, dtype=float)


def main():
    os.makedirs("outputs/exports", exist_ok=True)

    # 1. 22-year trends (SST, Kd490, Precipitation)
    sst_summary = load_giovanni_2003_2024("data/incoming/SST.2003-2024.csv")
    sst_summary["annual_sst"] = sst_summary["annual_vals"]
    sst_summary["proj_sst"] = sst_summary["proj_vals"]
    kd_summary = load_giovanni_2003_2024("data/incoming/Kd490.2003-2024.csv") if os.path.exists("data/incoming/Kd490.2003-2024.csv") else None
    gpm_summary = load_giovanni_2003_2024("data/incoming/prec-rain.2003-2024.csv") if os.path.exists("data/incoming/prec-rain.2003-2024.csv") else None

    # 2. Existing 15-series trend results
    trends_df = pd.read_csv("outputs/statistics/trend_results_all.csv")
    trends_list = trends_df.where(pd.notnull(trends_df), None).to_dict(orient="records")

    # 3. Watersheds GeoJSON (14 HydroBASINS polygons)
    ws_gdf = gpd.read_file("data/incoming/sea_watersheds.geojson")
    ws_gdf["geometry"] = ws_gdf["geometry"].simplify(0.03, preserve_topology=True)
    watersheds_geojson = json.loads(ws_gdf.to_json())

    # 4. Seagrass polygons (21,221 total; extract top 350 largest by AREA_SQKM for fast Web GIS)
    sg_gdf = gpd.read_file("data/incoming/sea_hotspot_zones.geojson")
    total_seagrass_count = len(sg_gdf)
    total_seagrass_area = round(float(sg_gdf["AREA_SQKM"].sum()), 2) if "AREA_SQKM" in sg_gdf.columns else 0.0

    sg_top = sg_gdf.sort_values("AREA_SQKM", ascending=False).head(350).copy()
    centroids = sg_top.geometry.centroid
    lons = centroids.x.to_numpy()
    lats = centroids.y.to_numpy()

    sst_vals = sample_nc_at_points("data/incoming/SST.DNA.2018-2024.nc", "MODISA_L3m_SST_Monthly_4km_R2019_0_sst", lons, lats)
    kd_vals = sample_nc_at_points("data/incoming/KD490.DNA.2018-2024.nc", "MODISA_L3m_KD_Mo_4km_R2022_0_Kd_490", lons, lats)
    gpm_vals = sample_nc_at_points("data/incoming/GPM.DNA.2018-2024.nc", "GPM_3IMERGM_07_precipitation", lons, lats)

    seagrass_points = []
    for idx, (_, row) in enumerate(sg_top.iterrows()):
        sst_v = None if np.isnan(sst_vals[idx]) else round(float(sst_vals[idx]), 2)
        kd_v = None if np.isnan(kd_vals[idx]) else round(float(kd_vals[idx]), 4)
        gpm_v = None if np.isnan(gpm_vals[idx]) else round(float(gpm_vals[idx]), 2)

        # Simple transparent risk heuristic from real NASA values
        score = 0
        if sst_v is not None and sst_v >= 29.0:
            score += 2
        elif sst_v is not None and sst_v >= 28.0:
            score += 1
        if kd_v is not None and kd_v >= 0.15:
            score += 2
        elif kd_v is not None and kd_v >= 0.08:
            score += 1
        if gpm_v is not None and gpm_v >= 0.30:
            score += 1

        risk = "High" if score >= 4 else ("Medium" if score >= 2 else "Low")
        seagrass_points.append(
            {
                "lat": round(float(lats[idx]), 4),
                "lon": round(float(lons[idx]), 4),
                "area_sqkm": round(float(row.get("AREA_SQKM", 0) or 0), 2),
                "family": str(row.get("FAMILY") or "Unknown"),
                "genus": str(row.get("GENUS") or "Unknown"),
                "sst": sst_v,
                "kd490": kd_v,
                "gpm": gpm_v,
                "risk": risk,
            }
        )

    payload = {
        "meta": {
            "total_seagrass_polygons": total_seagrass_count,
            "total_seagrass_area_sqkm": total_seagrass_area,
            "displayed_hotspots": len(seagrass_points),
            "total_watersheds": len(ws_gdf),
        },
        "sst_2003_2024": sst_summary,
        "kd490_2003_2024": kd_summary,
        "gpm_2003_2024": gpm_summary,
        "trends": trends_list,
        "watersheds_geojson": watersheds_geojson,
        "seagrass_hotspots": seagrass_points,
    }

    with open("data/processed/bluetrend_web_data.js", "w", encoding="utf-8") as f:
        f.write("window.BLUETREND_DATA = ")
        json.dump(payload, f, ensure_ascii=False)
        f.write(";")

    print(
        f"Exported web data: {total_seagrass_count} seagrass polygons, "
        f"{len(seagrass_points)} hotspots sampled, SST 2003-2024 p={sst_summary['p_value']}"
    )


if __name__ == "__main__":
    main()
