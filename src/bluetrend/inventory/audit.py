import json
import os
from datetime import datetime, timezone
import geopandas as gpd
import pandas as pd
import rasterio
import xarray as xr


def classify(ext: str) -> str:
    ext = ext.lower()
    if ext in [".csv", ".tsv", ".xlsx", ".xls", ".parquet"]:
        return "tabular"
    if ext in [".geojson", ".json", ".shp", ".gpkg", ".kml", ".gml"]:
        return "vector"
    if ext in [".tif", ".tiff", ".vrt"]:
        return "raster"
    if ext in [".nc", ".nc4", ".grib", ".zarr"]:
        return "multidimensional"
    if ext in [".md", ".txt", ".pdf", ".xml", ".yaml", ".yml"]:
        return "metadata_doc"
    if ext in [".py", ".ipynb", ".sh", ".ps1"]:
        return "code"
    return "unknown"


def run_audit(root_dir: str = ".") -> None:
    os.makedirs("metadata", exist_ok=True)
    os.makedirs("docs", exist_ok=True)

    now = datetime.now(timezone.utc).isoformat()
    inventory_rows = []
    catalog_rows = []
    validation_results = []

    exclude_dirs = {".venv", ".git", "metadata", "docs", "src", "tests", "config", "data", "outputs"}
    all_files = []
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for f in sorted(files):
            path = os.path.join(root, f).replace("\\", "/")
            if path.startswith("./"):
                path = path[2:]
            all_files.append(path)

    for p in sorted(all_files):
        size = os.path.getsize(p)
        ext = os.path.splitext(p)[1]
        cat = classify(ext)
        readable = True
        err = ""

        if cat == "tabular" and ext.lower() == ".csv":
            try:
                with open(p, "r", encoding="utf-8-sig") as fh:
                    meta_lines = [fh.readline().strip() for _ in range(7)]
                start_d = meta_lines[1].split(",", 1)[1].strip() if "," in meta_lines[1] else ""
                end_d = meta_lines[2].split(",", 1)[1].strip() if "," in meta_lines[2] else ""
                bbox = meta_lines[4].split(",", 1)[1].strip('"') if "," in meta_lines[4] else ""
                fill_line = meta_lines[6]
                df = pd.read_csv(p, skiprows=8)
                val_col = df.columns[1]
                fill_val = -9999.9 if "GPM" in fill_line else (-32767.0 if "KD" in fill_line else None)
                valid_cnt = (
                    int((df[val_col] != fill_val).sum())
                    if fill_val is not None
                    else int(df[val_col].notna().sum())
                )
                var_id = (
                    "precipitation"
                    if "GPM" in fill_line
                    else ("kd490" if "KD" in fill_line else "unknown")
                )
                units = (
                    "mm/hr (inferred from GPM_3IMERGM_07)"
                    if var_id == "precipitation"
                    else ("m^-1 (inferred from MODISA_L3m_KD)" if var_id == "kd490" else "unknown")
                )
                product = "GPM_3IMERGM_07" if var_id == "precipitation" else "MODISA_L3m_KD_Mo_4km_R2022_0"

                catalog_rows.append(
                    {
                        "dataset_id": os.path.splitext(os.path.basename(p))[0],
                        "source_file": p,
                        "data_type": "tabular_timeseries",
                        "source_provider": "NASA GES DISC / Giovanni",
                        "product_name": product,
                        "variable_id": var_id,
                        "units": units,
                        "time_start": start_d,
                        "time_end": end_d,
                        "temporal_resolution": "monthly",
                        "spatial_coverage": bbox,
                        "n_records": len(df),
                        "valid_records": valid_cnt,
                        "quality_flag": "pass" if valid_cnt == len(df) else "warning",
                    }
                )
                validation_results.append(
                    {
                        "file": p,
                        "status": "pass" if valid_cnt > 0 else "fail",
                        "n_records": len(df),
                        "valid_records": valid_cnt,
                        "notes": f"Giovanni monthly CSV, {len(df)} rows, {valid_cnt} valid",
                    }
                )
            except Exception as e:
                readable = False
                err = str(e)
                validation_results.append({"file": p, "status": "fail", "notes": err})

        elif cat == "vector":
            try:
                gdf = gpd.read_file(p)
                catalog_rows.append(
                    {
                        "dataset_id": os.path.splitext(os.path.basename(p))[0],
                        "source_file": p,
                        "data_type": "vector",
                        "source_provider": "unknown",
                        "product_name": os.path.basename(p),
                        "variable_id": "geometry",
                        "units": str(gdf.crs),
                        "time_start": "",
                        "time_end": "",
                        "temporal_resolution": "static",
                        "spatial_coverage": str(gdf.total_bounds.tolist()),
                        "n_records": len(gdf),
                        "valid_records": int(gdf.geometry.is_valid.sum()),
                        "quality_flag": "pass" if gdf.geometry.is_valid.all() else "warning",
                    }
                )
                validation_results.append(
                    {
                        "file": p,
                        "status": "pass" if gdf.geometry.is_valid.all() else "warning",
                        "crs": str(gdf.crs),
                        "features": len(gdf),
                        "valid_geoms": int(gdf.geometry.is_valid.sum()),
                    }
                )
            except Exception as e:
                readable = False
                err = str(e)
                validation_results.append({"file": p, "status": "fail", "notes": err})

        elif cat == "raster":
            try:
                with rasterio.open(p) as src:
                    catalog_rows.append(
                        {
                            "dataset_id": os.path.splitext(os.path.basename(p))[0],
                            "source_file": p,
                            "data_type": "raster_geotiff",
                            "source_provider": "NASA Giovanni (inferred)",
                            "product_name": os.path.basename(p),
                            "variable_id": os.path.splitext(os.path.basename(p))[0],
                            "units": "unknown_in_tif_header",
                            "time_start": "",
                            "time_end": "",
                            "temporal_resolution": "time_mean_static",
                            "spatial_coverage": str(list(src.bounds)),
                            "n_records": src.height * src.width,
                            "valid_records": "",
                            "quality_flag": "pass",
                        }
                    )
                    validation_results.append(
                        {
                            "file": p,
                            "status": "pass",
                            "crs": str(src.crs),
                            "shape": [src.height, src.width],
                            "nodata": src.nodata,
                        }
                    )
            except Exception as e:
                readable = False
                err = str(e)
                validation_results.append({"file": p, "status": "fail", "notes": err})

        elif cat == "multidimensional":
            try:
                ds = xr.open_dataset(p)
                v = [k for k in ds.data_vars if "bnds" not in k][0]
                attrs = ds[v].attrs
                lat_min, lat_max = float(ds["lat"].min()), float(ds["lat"].max())
                lon_min, lon_max = float(ds["lon"].min()), float(ds["lon"].max())
                catalog_rows.append(
                    {
                        "dataset_id": os.path.splitext(os.path.basename(p))[0],
                        "source_file": p,
                        "data_type": "netcdf_grid",
                        "source_provider": "NASA Giovanni",
                        "product_name": f"{attrs.get('product_short_name', '')} {attrs.get('product_version', '')}".strip(),
                        "variable_id": v,
                        "units": attrs.get("units", "unknown"),
                        "time_start": "",
                        "time_end": "",
                        "temporal_resolution": "time_mean_static",
                        "spatial_coverage": f"lat:{lat_min:.2f}..{lat_max:.2f}, lon:{lon_min:.2f}..{lon_max:.2f}",
                        "n_records": int(ds[v].size),
                        "valid_records": int(ds[v].notnull().sum()),
                        "quality_flag": "pass",
                    }
                )
                validation_results.append(
                    {
                        "file": p,
                        "status": "pass",
                        "variable": v,
                        "units": attrs.get("units", "unknown"),
                        "dims": dict(ds.sizes),
                    }
                )
                ds.close()
            except Exception as e:
                readable = False
                err = str(e)
                validation_results.append({"file": p, "status": "fail", "notes": err})

        inventory_rows.append(
            {
                "path": p,
                "filename": os.path.basename(p),
                "extension": ext,
                "size_bytes": size,
                "category": cat,
                "readable": readable,
                "error": err,
            }
        )

    pd.DataFrame(inventory_rows).to_csv("metadata/input_inventory.csv", index=False)
    pd.DataFrame(catalog_rows).to_csv("metadata/data_catalog.csv", index=False)
    with open("metadata/validation_report.json", "w", encoding="utf-8") as f:
        json.dump(
            {"generated_at": now, "total_files": len(inventory_rows), "results": validation_results},
            f,
            indent=2,
            ensure_ascii=False,
        )
    print(f"Audit complete: {len(inventory_rows)} files inventoried, {len(catalog_rows)} catalog entries.")


if __name__ == "__main__":
    run_audit()
