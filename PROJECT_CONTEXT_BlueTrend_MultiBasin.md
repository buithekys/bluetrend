# PROJECT_CONTEXT.md
# BlueTrend — Southeast Asia Multi-Basin Earth System Trend Analysis

> Tài liệu này là đặc tả ngữ cảnh dành cho AI Coding Agent. Hãy đọc toàn bộ trước khi kiểm tra dữ liệu hoặc viết code.
>
> **Tình trạng đầu vào:** Thư mục dự án có thể chỉ chứa các tệp dữ liệu rời rạc như CSV, Excel, GeoJSON, Shapefile, GeoPackage, GeoTIFF, NetCDF, GRIB và tài liệu metadata. Không được giả định chúng đã đúng chuẩn, đầy đủ hoặc sẵn sàng phân tích.
>
> **Nguyên tắc tối cao:** Kiểm kê trước, hiểu dữ liệu sau, rồi mới cấu trúc hóa và xử lý. Không xóa, ghi đè, đổi tên hoặc di chuyển dữ liệu gốc.

---

## 1. Project mission

**BlueTrend — Southeast Asia River Basin Earth System Trend Explorer** là ứng dụng phân tích xu hướng các biến của hệ thống Trái Đất trên **7 lưu vực sông trọng điểm Đông Nam Á**.

Ứng dụng cần giúp người dùng trả lời:
1. What is changing? Biến môi trường nào đang thay đổi?
2. Where is it changing? Sự thay đổi xảy ra ở lưu vực/khu vực nào?
3. How much is it changing? Tốc độ và mức độ thay đổi là bao nhiêu?
4. Is it statistically significant? Xu hướng có ý nghĩa thống kê hay không?

Các chức năng mục tiêu:
- Chọn một trong bảy lưu vực hoặc xem tổng quan nhiều lưu vực.
- Chọn biến môi trường và khoảng thời gian.
- Xem chuỗi thời gian, bản đồ và kết quả phân tích khi dữ liệu hỗ trợ.
- Ước lượng tốc độ thay đổi và kiểm định xu hướng.
- So sánh giữa các lưu vực khi dữ liệu tương thích.
- Hiển thị nguồn, đơn vị, độ phân giải, thời gian, phương pháp xử lý và giới hạn diễn giải.

**Danh sách tên chính thức, mã và ranh giới của bảy lưu vực chưa được xác nhận trong tài liệu này.** Không tự chọn, tự đặt tên hoặc tự tạo ranh giới. Hãy tìm trong dữ liệu/tài liệu đầu vào; nếu không có, đánh dấu cần người dùng xác nhận.

### Core challenge vs. project extensions

**Phần cốt lõi:** chọn biến Earth science, lấy dữ liệu theo khu vực/thời gian, tạo chuỗi thời gian, ước lượng trend, kiểm định ý nghĩa thống kê và trực quan hóa.

**Phần mở rộng:** so sánh nhiều lưu vực, bản đồ tương tác, phân tích tiểu vùng, xếp hạng theo từng biến và tổng hợp insight. Không để các phần mở rộng làm sai lệch kết quả phân tích cốt lõi.

---

## 2. Instructions to the AI Agent

Bạn là AI Engineering Assistant kiêm Data Engineering Assistant cho BlueTrend.

### 2.1. Việc đầu tiên: audit toàn bộ thư mục

1. Đọc file này.
2. Quét đệ quy toàn bộ thư mục dự án.
3. Liệt kê đường dẫn, tên, phần mở rộng, kích thước và khả năng đọc của từng tệp.
4. Phân loại sơ bộ: tabular, vector, raster, multidimensional/scientific, metadata/documentation, code, unknown.
5. Đọc metadata phù hợp:
   - CSV/Excel: cột, kiểu dữ liệu, số dòng, mẫu dữ liệu, missing values.
   - GeoJSON/Shapefile/GPKG: geometry, CRS, bounds, feature count, thuộc tính, validity.
   - GeoTIFF: CRS, transform, bounds, dimensions, bands, dtype, nodata, resolution, metadata.
   - NetCDF: dimensions, coordinates, variables, attributes, units, calendar, time coverage, spatial coverage, grid resolution.
   - GRIB/định dạng khác: xác định cách đọc; nếu không đọc được, ghi rõ lý do.
6. Đọc tài liệu metadata liên quan trước khi diễn giải dữ liệu.
7. Tạo báo cáo kiểm kê trước khi thay đổi cấu trúc.

### 2.2. Không giả định dữ liệu đã đúng chuẩn

Một tệp có phần mở rộng hợp lệ không đồng nghĩa dữ liệu đã sẵn sàng. Phải kiểm tra:
- Có đọc được và có dữ liệu thực không?
- Có biến, đơn vị và thời gian không?
- CRS và thông tin không gian có hợp lệ không?
- Có phủ các lưu vực cần nghiên cứu không?
- Có đủ số quan sát để phân tích trend không?
- Có missing values, duplicate records, outliers hoặc giá trị bất khả thi không?
- Các nguồn có thể so sánh được không?

Nếu thiếu thông tin, dùng `unknown`, `needs_review`, `warning` hoặc `blocked`. Không tự điền bằng giả định.

### 2.3. Bảo vệ dữ liệu gốc

- Không xóa, ghi đè, chỉnh sửa trực tiếp, đổi tên hoặc di chuyển file gốc.
- Không tự động reorganize input trong lần chạy đầu.
- Tạo inventory và đề xuất mapping đường dẫn trước.
- Nếu cần copy vào `data/raw/`, giữ nguyên file gốc và tên file, không tạo bản sao không cần thiết.
- Mọi bước xử lý phải tạo output mới trong `data/interim/` hoặc `data/processed/`.
- Ghi nguồn đầu vào, tham số và lịch sử xử lý.
- Không tải dữ liệu internet, gọi API có thể phát sinh chi phí hoặc yêu cầu credentials khi chưa được cho phép.
- Không đưa token, mật khẩu, Earthdata credentials hoặc API keys vào code/log.

### 2.4. Không tạo dữ liệu khoa học giả

- Không tự tạo observations để lấp missing data.
- Không tạo trend, p-value, bản đồ hoặc carbon estimate từ dữ liệu giả rồi trình bày như thật.
- Dữ liệu demo/test tổng hợp phải được gắn nhãn `SYNTHETIC / DEMO ONLY`, lưu tách biệt và không đưa vào kết quả nghiên cứu.
- Không nội suy missing values âm thầm.
- Không chuyển đổi đơn vị nếu chưa xác định đơn vị nguồn và công thức.

### 2.5. Báo cáo sau audit

Báo cáo:
1. Danh sách file và loại dữ liệu.
2. File đọc được/không đọc được.
3. Biến, đơn vị, thời gian và spatial coverage đã xác nhận.
4. File trùng lặp hoặc có vẻ là phiên bản khác.
5. Dữ liệu có thể dùng ngay.
6. Dữ liệu cần con người xác minh.
7. Đầu vào còn thiếu để nghiên cứu đủ bảy lưu vực.
8. Cấu trúc thư mục đề xuất.
9. Rủi ro và các bước tiếp theo.

Không chạy pipeline phân tích quy mô lớn trước khi hoàn thành audit và báo cáo.

---

## 3. Input formats and inspection requirements

Danh sách dưới đây là các định dạng có thể gặp, không phải khẳng định tất cả đều đã có.

### 3.1. Tabular: CSV, TSV, XLSX, XLS, Parquet

Có thể chứa SST, precipitation, soil moisture, evapotranspiration, air temperature hoặc thống kê theo basin.

Kiểm tra:
- Tên cột, kiểu dữ liệu, số dòng.
- Cột thời gian, timezone/calendar.
- Mã lưu vực.
- Biến và đơn vị.
- Dữ liệu là mean, sum, min, max, median hay statistic khác.
- Duplicate timestamps, missing periods, outliers.
- Rate hay accumulated quantity.
- Spatial aggregation đã được thực hiện hay chưa.

Không áp schema chuẩn trước khi hiểu dữ liệu gốc.

### 3.2. Vector: GeoJSON, JSON, SHP, GPKG, KML, GML

Có thể chứa basin boundaries, sub-basins, river lines, monitoring stations hoặc administrative boundaries.

Kiểm tra:
- CRS; nếu thiếu thì không tự đoán.
- Geometry type, validity, feature count, bounds.
- Thuộc tính tên/mã basin.
- Có đủ bảy lưu vực không?
- Polygon có overlap, empty geometry hoặc thiếu vùng không?
- Nguồn và phiên bản ranh giới.

Không mặc định ranh giới hành chính là ranh giới thủy văn. Không tự sửa geometry mà không lưu bản gốc và processing record.

### 3.3. Raster: GeoTIFF, TIFF, VRT và định dạng GDAL hỗ trợ

Có thể chứa SST, precipitation, soil moisture, evapotranspiration, land cover hoặc raster chỉ số.

Kiểm tra:
- CRS, transform, bounds, resolution.
- Band count và ý nghĩa band.
- dtype, nodata, scale factor, offset.
- Units, acquisition time/time range.
- Continuous hay categorical raster.
- Coverage các lưu vực.
- Pixel size có phù hợp mục tiêu không?

Continuous raster và categorical raster cần resampling khác nhau. Raster phân loại thường dùng nearest-neighbor. Không coi nodata là 0. Không tính diện tích bằng độ kinh/vĩ tuyến như thể đó là mét; dùng CRS chiếu phù hợp hoặc phương pháp geodesic.

### 3.4. Scientific multidimensional: NetCDF, NetCDF4, GRIB, Zarr

Đối với NetCDF, kiểm tra:
- Dimensions: `time`, `lat`, `lon`, `x`, `y`, `level`...
- Coordinates và CRS/spatial reference.
- Variables, attributes, `units`, `long_name`, `standard_name`.
- `scale_factor`, `add_offset`, `_FillValue`, `missing_value`.
- Calendar/time encoding.
- Grid type, spatial resolution, time coverage.
- Product/version và nguồn.

Không giả định tên biến giống nhau giữa các sản phẩm. Với dữ liệu lớn, ưu tiên lazy loading/chunking bằng xarray/Dask khi thích hợp; không load toàn bộ vào RAM nếu không cần. Không chuyển tất cả NetCDF sang CSV nếu làm mất cấu trúc đa chiều.

### 3.5. Documentation and metadata

Đọc các file TXT, MD, PDF, XML, JSON, YAML và tài liệu kèm theo để tìm:
- Data source/product/version.
- Biến, đơn vị và bảng mã raster.
- Citation/DOI.
- Phương pháp tải và xử lý.
- Ranh giới, mã basin và ghi chú nhóm.

---

## 4. Target folder structure

Đây là cấu trúc đích đề xuất, không phải cấu trúc được giả định đang tồn tại. Audit trước, sau đó mới tạo folder. Không phá vỡ các file đầu vào.

```text
BlueTrend/
├── PROJECT_CONTEXT.md
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
├── config/
│   ├── project.yaml
│   ├── basins.yaml
│   ├── variables.yaml
│   └── data_sources.yaml
├── data/
│   ├── incoming/
│   ├── raw/
│   │   ├── tabular/
│   │   ├── vector/
│   │   ├── raster/
│   │   ├── netcdf/
│   │   └── other/
│   ├── interim/
│   ├── processed/
│   │   ├── tabular/
│   │   ├── vector/
│   │   ├── raster/
│   │   └── cubes/
│   ├── sample/
│   └── external/
├── metadata/
│   ├── input_inventory.csv
│   ├── data_catalog.csv
│   ├── processing_log.csv
│   ├── validation_report.json
│   └── provenance/
├── outputs/
│   ├── tables/
│   ├── statistics/
│   ├── figures/
│   ├── maps/
│   ├── reports/
│   └── exports/
├── src/
│   └── bluetrend/
│       ├── inventory/
│       ├── data/
│       ├── spatial/
│       ├── temporal/
│       ├── analysis/
│       ├── visualization/
│       └── app/
├── tests/
│   ├── fixtures/
│   ├── test_inventory.py
│   ├── test_validation.py
│   ├── test_spatial.py
│   ├── test_temporal.py
│   └── test_trend.py
└── docs/
    ├── DATA_AUDIT_REPORT.md
    ├── DATA_DICTIONARY.md
    ├── METHODOLOGY.md
    ├── ASSUMPTIONS_AND_LIMITATIONS.md
    └── USER_GUIDE.md
```

Folder rules:
- `incoming/`: nơi nhận file đầu vào nếu cần.
- `raw/`: bản gốc bất biến.
- `interim/`: sản phẩm trung gian.
- `processed/`: dữ liệu chuẩn hóa đã kiểm tra.
- `outputs/`: kết quả phân tích và visualization.
- `metadata/`: catalog, inventory, provenance, validation.
- `sample/`: dữ liệu demo tổng hợp, tách khỏi dữ liệu nghiên cứu.

Không tạo bản sao trùng lặp không cần thiết. Nếu input đang ở vị trí hợp lý, có thể giữ nguyên và ghi đường dẫn trong catalog.

---

## 5. Basin configuration

Danh sách bảy lưu vực phải nằm trong cấu hình, không hard-code rải rác.

Ví dụ `config/basins.yaml`:

```yaml
basins:
  - basin_id: basin_01
    name: TO_BE_CONFIRMED
    country_or_countries: []
    boundary_file: null
    status: needs_review
  - basin_id: basin_02
    name: TO_BE_CONFIRMED
    country_or_countries: []
    boundary_file: null
    status: needs_review
  - basin_id: basin_03
    name: TO_BE_CONFIRMED
    country_or_countries: []
    boundary_file: null
    status: needs_review
  - basin_id: basin_04
    name: TO_BE_CONFIRMED
    country_or_countries: []
    boundary_file: null
    status: needs_review
  - basin_id: basin_05
    name: TO_BE_CONFIRMED
    country_or_countries: []
    boundary_file: null
    status: needs_review
  - basin_id: basin_06
    name: TO_BE_CONFIRMED
    country_or_countries: []
    boundary_file: null
    status: needs_review
  - basin_id: basin_07
    name: TO_BE_CONFIRMED
    country_or_countries: []
    boundary_file: null
    status: needs_review
```

Có thể bổ sung `official_name`, `aliases`, `basin_area_km2`, `boundary_source`, `boundary_version`, `boundary_crs`, `notes`. Không điền tên, diện tích, quốc gia hoặc nguồn ranh giới khi chưa có bằng chứng.

---

## 6. Canonical data model

Tạo data dictionary sau khi audit và ánh xạ dữ liệu thực tế vào schema chuẩn. Không ép mọi loại dữ liệu vào một bảng nếu làm mất thông tin.

### 6.1. Shared metadata

Khi xác định được, sản phẩm dẫn xuất nên ghi:
- `dataset_id`
- `source_file`
- `source_provider`
- `product_name`
- `product_version`
- `variable_id`
- `variable_name`
- `units`
- `basin_id`
- `time_start`, `time_end`
- `temporal_resolution`
- `spatial_resolution`
- `aggregation_method`
- `processing_version`
- `created_at`
- `quality_flag`

Không xác định được thì để null/unknown và ghi nhận trong report.

### 6.2. Normalized time-series table

Schema gợi ý dạng long-format:

| Field | Ý nghĩa |
|---|---|
| `basin_id` | Mã lưu vực |
| `time` | Mốc thời gian |
| `variable_id` | Mã biến |
| `value` | Giá trị |
| `units` | Đơn vị |
| `statistic` | mean/sum/min/max/median... |
| `valid_observation_count` | Số pixel/quan sát hợp lệ nếu có |
| `valid_data_fraction` | Tỷ lệ dữ liệu hợp lệ nếu tính được |
| `source_dataset_id` | Dataset nguồn |
| `quality_flag` | Cờ chất lượng |

### 6.3. Vector, raster and NetCDF

- Giữ nguyên vector/raster/NetCDF nguồn.
- Có thể tạo GeoPackage tổng hợp basin polygons nếu CRS/schema phù hợp.
- Giữ `basin_id` duy nhất và ổn định.
- Chỉ clip/reproject/aggregate khi cần và ghi lại phương pháp.
- Mỗi raster output phải có CRS, transform, resolution, nodata, units, source và processing steps.
- NetCDF output phải giữ dimensions, coordinates, time/calendar, attributes, fill values và CRS/spatial reference khi có.

---

## 7. Data quality and validation

Mỗi kiểm tra trả về `pass`, `warning`, `fail` hoặc `unknown`, kèm lý do.

### File integrity
- File tồn tại, không rỗng, đọc được.
- Không bị truncated/corrupt.
- Các file phụ trợ bắt buộc (ví dụ Shapefile) có đầy đủ.

### Temporal quality
- Parse time thành công.
- Thứ tự thời gian hợp lệ.
- Duplicate timestamps.
- Tần suất hourly/3-hourly/daily/monthly/annual/irregular.
- Missing periods.
- Calendar trong NetCDF.
- Không trộn tần suất nếu chưa có quy tắc aggregation.

### Spatial quality
- CRS xác định được.
- Bounds hợp lệ.
- Dữ liệu giao với basin.
- Resolution phù hợp.
- Geometry validity và raster alignment.
- Không tính zonal statistics trước khi xác nhận CRS, transform và polygon.

### Semantic quality
- Đúng biến và đơn vị.
- Phân biệt rate với accumulation.
- Phân biệt instantaneous value với temporal mean.
- Phân biệt land surface temperature với sea surface temperature.
- Kiểm tra scale factor/offset và miền giá trị.
- Không kết hợp sản phẩm cùng tên biến nhưng khác định nghĩa nếu chưa chuẩn hóa.

### Coverage and comparability
- Dataset phủ basin nào?
- Khoảng thời gian nào?
- Có đủ quan sát không?
- Các basin có cùng product, units, period, resolution và aggregation không?
- Nếu không tương thích, báo cáo riêng và nêu hạn chế; không tạo ranking gây hiểu lầm.

---

## 8. Scientific workflow

### 8.1. Preparation
1. Inventory.
2. Đọc metadata và tài liệu.
3. Xác định basin boundaries.
4. Xác định variables, units, temporal resolution.
5. Kiểm tra CRS, bounds, coverage.
6. Chuẩn hóa và giữ provenance.
7. Tạo time series theo basin-variable.
8. Tính valid-data coverage và quality flags.

### 8.2. Spatial aggregation

Với raster/grid trong polygon, có thể tính mean, median, min/max, sum hoặc percentile. Không mặc định mean phù hợp mọi biến.

- Precipitation: phân biệt rate (ví dụ mm/hour, kg m⁻² s⁻¹) với accumulated depth (mm). Cộng hay lấy trung bình tùy định nghĩa sản phẩm và mục tiêu.
- Temperature: thường tính mean/median; không cộng nhiệt độ.
- Ratio/index: kiểm tra định nghĩa và miền giá trị.
- Area: dùng CRS chiếu phù hợp hoặc geodesic calculation, không tính trực tiếp từ degree như mét.

### 8.3. Trend analysis

Các phương pháp có thể sử dụng:
- Linear regression slope.
- Mann-Kendall trend test.
- Sen's slope.
- Confidence intervals nếu phương pháp hỗ trợ.
- Seasonal Mann-Kendall khi có mùa vụ và dữ liệu phù hợp.

Mỗi kết quả cần có:
- `basin_id`, `variable_id`;
- time range, temporal resolution;
- sample size;
- slope và slope units;
- p-value, alpha;
- trend direction;
- confidence interval nếu có;
- method;
- data quality/limitations.

Diễn giải:
- Slope dương/âm thể hiện hướng và tốc độ theo đơn vị thời gian.
- p-value < alpha là bằng chứng thống kê chống lại giả thuyết không có trend theo phép kiểm định, không chứng minh nguyên nhân.
- Non-significant không có nghĩa chắc chắn không thay đổi.
- Không suy diễn tương quan thành nhân quả.
- Chuỗi ngắn/thiếu dữ liệu có thể có statistical power thấp.
- Dữ liệu tháng/ngày có mùa vụ hoặc autocorrelation cần được xem xét.
- Khi kiểm định nhiều biến × nhiều basin, cân nhắc multiple-testing correction.

### 8.4. Cross-basin comparison

Chỉ so sánh khi biến, đơn vị, thời gian, tần suất/aggregation và phương pháp tương thích.

Có thể so sánh slope gốc, standardized slope hoặc phần trăm thay đổi nếu baseline hợp lệ, trend direction, p-value, sample size và coverage.

Không xếp hạng chỉ theo p-value. Không so sánh slope có đơn vị/cách tổng hợp khác nhau.

### 8.5. Spatial visualization

Có thể hiển thị:
- Basin boundaries.
- Giá trị thống kê của biến.
- Slope/trend direction.
- Significance category.
- Vùng thiếu dữ liệu.

Phân biệt rõ `not significant`, `insufficient data` và `not analyzed`. Không tô màu một basin như tăng/giảm mạnh nếu chưa có kết quả đạt quality checks.

---

## 9. Expected outputs and output standards

**Không có một bộ output duy nhất bắt buộc cho mọi loại input.** Output đúng chuẩn phụ thuộc loại dữ liệu, mục tiêu, resolution và phương pháp. Agent phải audit trước rồi mới xác định output nào khả thi.

### 9.1. First reliable version: expected deliverables

| Output | Format gợi ý | Mục đích |
|---|---|---|
| Input inventory | CSV | Danh sách toàn bộ input files |
| Data catalog | CSV/JSON | Dataset, biến, đơn vị, nguồn, coverage |
| Validation report | JSON/Markdown | Kết quả kiểm tra chất lượng |
| Basin boundaries | GeoJSON/GPKG | Ranh giới basin đã xác minh |
| Normalized time series | CSV/Parquet | Chuỗi theo basin-variable |
| Trend results | CSV/Parquet | Kết quả kiểm định trend |
| Processing log | CSV/JSON | Lịch sử biến đổi |
| Data dictionary | Markdown | Schema, ý nghĩa trường, units |

Chỉ tạo khi đủ dữ liệu. Nếu chưa có boundary hoặc basin mapping, không tạo kết quả basin-level giả.

### 9.2. Optional outputs

| Output | Format | Điều kiện |
|---|---|---|
| Zonal statistics | CSV/Parquet | Có raster/grid và basin polygons hợp lệ |
| Clipped rasters | GeoTIFF | Cần bản đồ/phân tích raster theo vùng |
| Aggregated data cube | NetCDF | Cần giữ cấu trúc đa chiều |
| Basin comparison | CSV | Chuỗi tương thích |
| Trend maps | GeoPackage/GeoJSON + style hoặc PNG | Có kết quả hợp lệ |
| Figures | PNG/SVG/HTML | Có dữ liệu đã kiểm tra |
| Technical report | Markdown/PDF | Có kết quả và provenance |

### 9.3. Naming convention

Ví dụ:
- `input_inventory_YYYYMMDD.csv`
- `data_catalog.csv`
- `validation_report_YYYYMMDD.json`
- `timeseries_<variable_id>.parquet`
- `trend_results_<variable_id>.csv`
- `basin_comparison_<variable_id>.csv`
- `processing_log.csv`

Không dùng tên mơ hồ như `final_final2.csv`. Không ghi đè output cũ khi chưa xác nhận.

### 9.4. Minimum trend-result schema

| Field | Description |
|---|---|
| `basin_id` | Basin identifier |
| `variable_id` | Variable identifier |
| `time_start`, `time_end` | Analysis period |
| `temporal_resolution` | Frequency |
| `n_observations` | Valid sample count |
| `slope`, `slope_units` | Trend estimate and units |
| `sen_slope` | Sen's slope, if computed |
| `p_value` | Test p-value |
| `alpha` | Significance threshold |
| `trend_direction` | increasing/decreasing/no_detected_trend/undetermined |
| `significance` | significant/not_significant/insufficient_data |
| `method` | Statistical method |
| `confidence_low`, `confidence_high` | Optional bounds |
| `data_coverage` | Coverage/quality |
| `notes` | Caveats |

Không điền slope/p-value bằng 0 nếu không tính được.

### 9.5. GeoTIFF standards
- CRS, transform, pixel size và nodata đúng.
- Units/variable được ghi trong metadata hoặc tài liệu đi kèm.
- Band descriptions rõ ràng.
- Phân biệt continuous/categorical.
- Scale/offset được xử lý hoặc giữ nguyên có giải thích.
- File mở lại được sau khi ghi.
- Có source và processing record.

### 9.6. NetCDF standards
- Dimensions/coordinates hợp lệ.
- Time/calendar rõ.
- Variable attributes như `long_name`, `units` khi xác định được.
- Fill values nhất quán.
- CRS/spatial reference được giữ hoặc mô tả.
- Global attributes có source, creation time và processing history.

CSV phù hợp cho time series đã aggregate theo basin; NetCDF phù hợp để giữ dữ liệu lưới nhiều chiều. Không chuyển đổi định dạng chỉ vì muốn tất cả file giống nhau.

---

## 10. Application requirements

Ứng dụng dự kiến dùng Python + Streamlit. Nếu repository đã có framework phù hợp, hãy đánh giá trước khi thay thế.

### Page 1 — Data & Basin Overview
- Bản đồ 7 basin sau khi danh sách được xác nhận.
- Trạng thái dữ liệu từng basin.
- Biến, thời gian và nguồn có sẵn.
- Cảnh báo missing/incompatible data.

### Page 2 — Basin Explorer
- Chọn basin, biến và thời gian.
- Hiển thị boundary/map và time series.
- Hiển thị metadata, units, data coverage.

### Page 3 — Trend Analysis
- Slope, Sen's slope, p-value, alpha, sample size.
- Method và interpretation.
- Phân biệt non-significant với insufficient data.

### Page 4 — Cross-Basin Comparison
- Chỉ so sánh các basin có input tương thích.
- Bảng/biểu đồ so sánh.
- Giải thích basin nào bị loại và vì sao.
- Không ranking khi không đủ cơ sở.

### Page 5 — Data Provenance & Methodology
- Dataset/product/source/version.
- Units, spatial/temporal resolution.
- Processing history.
- Assumptions and limitations.

UX:
- Mọi chart axis có units.
- Hiển thị source và time range.
- Có loading/error/empty states.
- Không che giấu quality warnings.
- Hỗ trợ dữ liệu lớn; không load toàn bộ vào RAM.
- Dùng cache khi phù hợp.

---

## 11. Suggested technical stack

Chỉ thêm thư viện khi cần và kiểm tra môi trường/OS trước khi cài.

**Data:** `pandas`, `numpy`, `scipy`, `xarray`, `netCDF4`, `h5netcdf`, `dask` (nếu cần), `pyarrow`.

**Geospatial:** `geopandas`, `shapely`, `pyproj`, `rasterio`, `rioxarray`, `GDAL` (nếu cần).

**Statistics:** `pymannkendall`, `scipy`, `statsmodels`.

**App/visualization:** `streamlit`, `plotly`, `folium`, `streamlit-folium`, `matplotlib`.

**Testing/quality:** `pytest`, optional `pandera`, `pydantic`, `ruff`.

Không cài toàn bộ danh sách máy móc. Một số thư viện địa không gian có system dependencies; ghi rõ cách cài tương thích trong README và requirements.

---

## 12. NASA and external data provenance

Nguồn có thể gặp, không giới hạn:
- MODIS: một số sản phẩm nhiệt độ bề mặt/đại dương.
- GPM IMERG: precipitation.
- MERRA-2: atmospheric reanalysis.
- GLDAS: land-surface variables.
- Landsat: Earth observation imagery.
- Các Earth science datasets khác được Challenge Resources hoặc phương pháp nghiên cứu cho phép.

Đây là nguồn tiềm năng, không khẳng định tất cả đã có trong thư mục hoặc đều bắt buộc.

Với mỗi dataset, ghi provider, full product name, short name, version/collection, DOI/URL, access date, resolution, units, variable, processing, license/terms, citation và limitations.

Nếu Global Awards yêu cầu ít nhất một NASA dataset nằm trong Resources tab của Challenge, phải xác minh trực tiếp từ trang Challenge và lưu bằng chứng. Không suy ra eligibility chỉ vì dataset có nguồn gốc NASA.

---

## 13. Reproducibility and security

- Không commit credentials hoặc `.env`.
- `.env.example` chỉ có tên biến và placeholder.
- Ghi phiên bản thư viện và môi trường Python.
- Ghi processing parameters và random seeds khi có.
- Dùng relative paths/`pathlib`, không hard-code đường dẫn máy cá nhân.
- Tách analysis logic khỏi Streamlit UI để kiểm thử.
- Mỗi bước phải chạy lại được hoặc giải thích được.
- Không ghi đè output tự động.
- Ghi log lỗi và processing log.

---

## 14. Implementation phases

### Phase 0 — Repository and input audit (must be first)
Tạo:
- `metadata/input_inventory.csv`
- `metadata/data_catalog.csv`
- `metadata/validation_report.json`
- `docs/DATA_AUDIT_REPORT.md`
- `docs/DATA_DICTIONARY.md`

Không chạy trend analysis trước khi audit xong.

### Phase 1 — Safe organization
- Tạo folder structure.
- Giữ nguyên input files.
- Đề xuất mapping từng file.
- Chỉ copy/reorganize sau audit và không overwrite.
- Tạo config placeholder cho 7 basin nếu chưa xác nhận.

### Phase 2 — Loaders and validation
- Loader riêng cho CSV, vector, raster, NetCDF.
- Chuẩn hóa metadata.
- Validation report.
- Unit tests.

### Phase 3 — Basin and time-series preparation
Chỉ khi có basin boundaries hợp lệ và dữ liệu định vị được:
- Validate boundaries.
- Spatial subset/zonal statistics.
- Temporal aggregation.
- Normalized time series.
- Provenance và quality flags.

### Phase 4 — Trend engine
- Linear regression.
- Mann-Kendall.
- Sen's slope.
- Seasonal analysis khi phù hợp.
- Confidence intervals nếu hỗ trợ.
- Unit tests với test data có kết quả kỳ vọng đã biết.

### Phase 5 — Comparative analysis
- Basin-variable comparison.
- Compatibility checks.
- Slope units/standardization.
- Multiple-testing considerations.
- Không ranking nếu thiếu cơ sở.

### Phase 6 — Streamlit app
- Data overview.
- Basin explorer.
- Trend analysis.
- Cross-basin comparison.
- Provenance/methodology.

### Phase 7 — Documentation and release
- README, data dictionary, methodology.
- Assumptions/limitations.
- User guide.
- Reproducible run instructions.

---

## 15. What can be implemented now vs. what needs confirmation

### Can implement immediately
- Recursive repository scanner.
- File-format detection.
- CSV/Excel/GeoJSON/Shapefile/GPKG/GeoTIFF/NetCDF metadata inspectors.
- Inventory/catalog generation.
- Validation framework.
- Folder structure.
- Config schema.
- Tests using synthetic fixtures clearly labeled as test data.
- Streamlit skeleton with empty states.
- Trend functions and independent tests.

### Requires real input or human confirmation
- Official names and list of 7 river basins.
- Authoritative basin boundaries and source/version.
- Variables the team will analyze.
- Dataset source/product/version where unclear.
- Units when metadata is missing/ambiguous.
- Temporal aggregation choices.
- Spatial resolution suitability.
- Quality thresholds.
- Scientific basis for cross-basin comparisons.
- Ecological/causal interpretations.

### Must never be fabricated
- Basin names/boundaries.
- Dataset source/version.
- Units.
- Missing observations.
- Trend statistics and p-values.
- Confidence intervals.
- Rankings.
- Ecological conclusions.

---

## 16. Definition of Done

### Data readiness
- [ ] All input files inventoried.
- [ ] Usable files have catalog entries.
- [ ] Raw files preserved.
- [ ] Variables/units documented or marked unknown.
- [ ] Temporal and spatial coverage documented.
- [ ] Basin boundaries verified and linked to stable IDs.
- [ ] Warnings/failures visible.

### Analytical readiness
- [ ] Time series traceable to source.
- [ ] Spatial/temporal aggregation documented.
- [ ] Missing data not silently converted to zero.
- [ ] Trend methods tested.
- [ ] Slope units and p-values correct.
- [ ] Insufficient data distinct from non-significant.
- [ ] Cross-basin comparisons use compatible inputs.

### Application readiness
- [ ] Select basin and variable.
- [ ] Inspect time series and trend statistics.
- [ ] Maps use verified boundaries and CRS.
- [ ] Source and methodology visible.
- [ ] Empty/error/insufficient-data states handled.
- [ ] Synthetic data never presented as real.

### Reproducibility
- [ ] Processing logs exist.
- [ ] Environment/run instructions documented.
- [ ] Tests pass.
- [ ] Another user can reproduce main outputs.

---

## 17. First prompt to the AI Agent

Sau khi đặt file này vào thư mục dự án, dùng prompt:

```text
Read PROJECT_CONTEXT.md completely before taking any action.

You are the AI engineering and data engineering assistant for BlueTrend.

The project directory may contain only raw or partially processed input files
such as CSV, Excel, GeoJSON, Shapefile, GeoPackage, GeoTIFF, NetCDF, GRIB,
and metadata documents. Do not assume that the files are correctly organized
or analysis-ready.

Your first task is PHASE 0: REPOSITORY AND INPUT AUDIT.

1. Recursively inspect the entire project directory.
2. Do not delete, overwrite, rename, or move any input file.
3. Identify every file, its format, size, readability, and likely role.
4. Inspect metadata and schemas using suitable libraries.
5. For geospatial/scientific data, inspect CRS, bounds, resolution, variables,
   dimensions, units, timestamps, nodata/fill values, and coverage when available.
6. Identify which of the seven river basins are represented. Do not invent
   basin names or boundaries. If the official list is absent, request confirmation.
7. Assess whether the inputs are sufficient for spatial aggregation,
   time-series construction, trend analysis, and cross-basin comparison.
8. Create an input inventory, data catalog, validation report, and audit report.
9. Propose a safe target folder structure and a file-by-file organization plan.
10. Separate confirmed facts, inferences, unknowns, warnings, and blockers.

Do not begin large-scale processing or create scientific results yet.

Do not fabricate observations, units, metadata, basin boundaries, trend statistics,
p-values, or maps. Synthetic data may only be used in isolated tests and must be
labeled SYNTHETIC / TEST ONLY.

At the end, provide:
- concise audit summary;
- table of all input files and status;
- recommended target structure;
- missing/ambiguous information;
- prioritized next implementation steps.

Wait for human review before moving or reorganizing original input files.
```

---

## 18. Final operating principle

BlueTrend is a scientific data analysis application, not merely a dashboard that plots arbitrary files.

Always preserve the distinction between:
1. What the source data actually contains.
2. What can be derived through documented processing.
3. What statistical analysis supports.
4. What remains uncertain or cannot yet be concluded.

When in doubt, report uncertainty and request confirmation instead of silently making a scientific assumption.
