# BlueTrend — Southeast Asia Multi-Basin Earth System Trend Explorer

## Cấu trúc thư mục

- `config/` — Cấu hình lưu vực (`basins.yaml`) và tham số dự án.
- `data/incoming/` — Nơi đặt các tệp dữ liệu mới tải về (CSV 2003–2024, NetCDF đa chiều, GeoJSON/Shapefile lưu vực thật) trước khi kiểm kê.
- `data/raw/` — Bản gốc bất biến (`tabular/`, `vector/`, `raster/`, `netcdf/`, `other/`). *Lưu ý: các tệp gốc ban đầu hiện vẫn được giữ nguyên tại thư mục gốc.*
- `data/interim/` — Dữ liệu trung gian.
- `data/processed/` — Dữ liệu đã chuẩn hóa (`tabular/timeseries_all.parquet`, `vector/`, `raster/`, `cubes/`).
- `metadata/` — Kiểm kê (`input_inventory.csv`), danh mục (`data_catalog.csv`), log xử lý (`processing_log.csv`), báo cáo kiểm tra (`validation_report.json`).
- `outputs/` — Kết quả phân tích (`statistics/trend_results_all.csv`, `figures/`, `maps/`, `reports/`).
- `src/bluetrend/` — Mã nguồn tách biệt theo module (`inventory/`, `data/`, `spatial/`, `temporal/`, `analysis/`, `visualization/`, `app/`).
- `docs/` — Tài liệu kiểm kê và từ điển dữ liệu (`DATA_AUDIT_REPORT.md`, `DATA_DICTIONARY.md`).

## Quy trình khi bổ sung input mới

1. Đặt tệp mới vào `data/incoming/` (hoặc đúng thư mục con trong `data/raw/`).
2. Cập nhật `config/basins.yaml` nếu thêm vùng/lưu vực mới.
3. Chạy lại pipeline theo thứ tự:
   ```powershell
   .\.venv\Scripts\python.exe src\bluetrend\inventory\audit.py
   .\.venv\Scripts\python.exe src\bluetrend\data\loader.py
   .\.venv\Scripts\python.exe src\bluetrend\analysis\trend.py
   ```
4. Khởi chạy ứng dụng Streamlit:
   ```powershell
   .\.venv\Scripts\streamlit.exe run src\bluetrend\app\app.py
   ```
