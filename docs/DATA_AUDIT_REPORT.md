# Data Audit Report — BlueTrend Multi-Basin

**Generated:** 2026-11-14  
**Scope:** Recursive inventory and validation of all 26 input files in `D:\DevDesktop\Kathon` (excluding `.venv`).

---

## 1. Summary of Inventoried Files

| Category | Count | Readable | Notes |
|---|---:|---:|---|
| Tabular (`.csv`) | 15 | 15 / 15 | NASA Giovanni monthly area-averaged time series (2018-01 to 2024-12, 84 months each) |
| Vector (`.geojson`) | 2 | 2 / 2 | `sea_coastal_roi.geojson` (coastal/country ROI), `sea_hotspot_zones.geojson` (1 bounding polygon) |
| Raster (`.tif`) | 3 | 3 / 3 | `KD490sea.tif`, `SST..tif`, `pre-est.tif` (2D static/time-mean GeoTIFFs, EPSG:4326) |
| Multidimensional (`.nc`) | 3 | 3 / 3 | `kd490_sea.nc`, `SST.nc`, `prec_est.nc` (2D lat/lon grids, no time dimension) |
| Metadata / Docs (`.md`, `.txt`) | 3 | 3 / 3 | `PROJECT_CONTEXT_BlueTrend_MultiBasin.md`, `requirements.txt`, `prov.postprocess...txt` |
| **Total** | **26** | **26 / 26** | All files readable |

Full machine-readable inventory: [input_inventory.csv](file:///D:/DevDesktop/Kathon/metadata/input_inventory.csv)  
Data catalog: [data_catalog.csv](file:///D:/DevDesktop/Kathon/metadata/data_catalog.csv)  
Validation report: [validation_report.json](file:///D:/DevDesktop/Kathon/metadata/validation_report.json)

---

## 2. Confirmed Variables, Units, Time & Spatial Coverage

### 2.1. Precipitation (`GPM_3IMERGM_07_precipitation`)
- **Provider / Source:** NASA GES DISC / Giovanni (`GPM_3IMERGM` v07)
- **Units:** `mm/hr` (rate, confirmed in `prec_est.nc`; CSV headers list fill value `-9999.9`)
- **Temporal Coverage:** `2018-01-01` to `2024-12-31` (monthly, 84 observations per file)
- **CSV Files (8):**
  1. `DongNamA.csv` — Regional SEA bounding box (`92.05,-10.95,140.95,28.45`)
  2. `Luu vuc Song Irrawaddy & Salween.csv` (`94.55,16.05,98.45,21.95`)
  3. `Luu vuc song Kampar & Pahang.csv` (`100.55,-0.95,103.45,4.45`)
  4. `Luu vuc song Kapuas & Mahakam.csv` (`109.55,-2.45,117.45,1.45`)
  5. `Luu vuc song Mekong & Chao Phraya.csv` (`100.05,8.55,107.95,21.95`)
  6. `Luu vuc Sông Thu Bồn & Sông Côn.csv` (`107.55,13.55,109.25,15.95`)
  7. `Song Cagayan & Kinabatangan.csv` (`116.55,5.05,122.45,18.45`)
  8. `Song Hong-Thai Binh.csv` (`102.55,19.55,107.95,23.45`)
- **Gridded Files:** `prec_est.nc` (395×490, `0.1°` resolution), `pre-est.tif` (395×490, EPSG:4326) — static 2D time-mean grids.

### 2.2. Diffuse Attenuation Coefficient at 490 nm (`MODISA_L3m_KD_Mo_4km_R2022_0_Kd_490`)
- **Provider / Source:** NASA OB.DAAC / Giovanni (`MODISA_L3m_KD` R2022.0)
- **Units:** `m^-1` (confirmed in `kd490_sea.nc`; CSV fill value `-32767`)
- **Temporal Coverage:** `2018-01-01` to `2024-12-31` (monthly, 84 observations per file)
- **CSV Files (7 coastal/marine regions):**
  1. `Bien Andaman.csv`
  2. `Bien Sulawesi.csv`
  3. `Central Coast.csv`
  4. `Indonesian Archipelago.csv`
  5. `Strait of Malacca.csv`
  6. `Vinh Thai Lan & Tay Nam Bo.csv`
  7. `VinhBacBo.csv`
- **Gridded Files:** `kd490_sea.nc` (948×1176, `0.04167°` ~4km), `KD490sea.tif` (948×1176, EPSG:4326) — static 2D time-mean grids.

### 2.3. Sea Surface Temperature (`MODISA_L3m_SST_Monthly_4km_R2019_0_sst`)
- **Provider / Source:** NASA OB.DAAC / Giovanni (`MODISA_L3m_SST_Monthly_4km` R2019.0)
- **Units:** `C` (degrees Celsius, confirmed in `SST.nc`)
- **Gridded Files:** `SST.nc` (948×1176, `0.04167°`), `SST..tif` (948×1176, EPSG:4326) — static 2D time-mean grids.
- **Note:** No SST CSV time series are present in the input directory.

---

## 3. Key Findings, Gaps & Risks

1. **Basin Boundaries:** The 7 river basins are represented in the precipitation CSVs as **rectangular bounding boxes** (`User Bounding Box` in Giovanni). `sea_coastal_roi.geojson` contains administrative/coastal country polygons, and `sea_hotspot_zones.geojson` contains a single regional box (`SEA_sea_region`). **True hydrological basin polygon shapefiles/GeoJSONs are not present.** Bounding boxes are used as spatial approximations and must be flagged as `needs_review` / `approximate_bbox`.
2. **Static Gridded Files:** `SST.nc`, `kd490_sea.nc`, `prec_est.nc` and their `.tif` counterparts have **no `time` dimension** (they are 2D time-mean composites). Therefore, pixel-level trend analysis cannot be computed from these `.nc`/`.tif` files; trend analysis must use the 15 monthly CSV time series.
3. **Original Files Preserved:** All 26 original files remain untouched in the root directory.
