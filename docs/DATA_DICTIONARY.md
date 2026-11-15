# Data Dictionary — BlueTrend Multi-Basin

## 1. Normalized Time-Series Schema (`data/processed/tabular/timeseries_all.parquet`)

| Field | Type | Description |
|---|---|---|
| `basin_id` | string | Stable identifier for the river basin or marine region (e.g., `basin_01`..`basin_07`, `marine_01`..`marine_07`, `region_sea`) |
| `basin_name` | string | Human-readable name derived from source filename |
| `region_type` | string | `river_basin`, `marine_region`, or `regional_overview` |
| `time` | datetime64 | Monthly timestamp (`YYYY-MM-01`) |
| `variable_id` | string | `precipitation` or `kd490` |
| `value` | float64 | Area-averaged monthly value (fill values replaced with `NaN`) |
| `units` | string | `mm/hr` for precipitation; `m^-1` for kd490 |
| `statistic` | string | `area_mean` |
| `source_dataset_id` | string | Source CSV filename stem |
| `product_name` | string | `GPM_3IMERGM_07` or `MODISA_L3m_KD_Mo_4km_R2022_0` |
| `quality_flag` | string | `pass` or `missing_fill` |

## 2. Trend Results Schema (`outputs/statistics/trend_results_all.csv`)

| Field | Type | Description |
|---|---|---|
| `basin_id` | string | Basin or marine region identifier |
| `basin_name` | string | Human-readable name |
| `region_type` | string | `river_basin`, `marine_region`, or `regional_overview` |
| `variable_id` | string | `precipitation` or `kd490` |
| `time_start` | string | Start date (`YYYY-MM-DD`) |
| `time_end` | string | End date (`YYYY-MM-DD`) |
| `temporal_resolution` | string | `monthly` |
| `n_observations` | int | Number of valid (non-NaN) monthly observations |
| `slope` | float64 | OLS linear regression slope (units per year) |
| `slope_units` | string | e.g., `mm/hr/year` or `m^-1/year` |
| `sen_slope` | float64 | Theil-Sen / Mann-Kendall Sen's slope (units per year) |
| `p_value` | float64 | Mann-Kendall two-sided p-value |
| `alpha` | float64 | Significance threshold (`0.05`) |
| `trend_direction` | string | `increasing`, `decreasing`, `no_detected_trend`, or `undetermined` |
| `significance` | string | `significant`, `not_significant`, or `insufficient_data` |
| `method` | string | `Mann-Kendall + Sen's Slope + OLS` |
| `data_coverage` | float64 | Fraction of valid observations (`n_observations / 84`) |
| `notes` | string | Caveats (e.g., bounding-box approximation, seasonality) |
