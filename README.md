# BlueTrend — Southeast Asia Seagrass & Watershed Monitor

Ứng dụng Web GIS giám sát phân bố **21.221 thảm cỏ biển Đông Nam Á**, áp lực môi trường từ **14 lưu vực sông HydroBASINS** và các biến vệ tinh **NASA (MODIS-Aqua SST, Kd490, GPM IMERG 2003–2024)** nhằm phát hiện xu hướng và cảnh báo vùng cần ưu tiên bảo vệ.

## Cấu trúc dự án

- `index.html` — Giao diện Web GIS chính (Leaflet + Chart.js + Tailwind, dùng OpenStreetMap miễn phí).
- `data/incoming/` — Dữ liệu đầu vào chính (`SST.2003-2024.csv`, `Kd490.2003-2024.csv`, `prec-rain.2003-2024.csv`, `sea_hotspot_zones.geojson`, `sea_watersheds.geojson`, và 3 tệp `.nc`).
- `data/raw/` — Dữ liệu gốc ban đầu (`tabular/`, `vector/`, `raster/`, `netcdf/`, `other/`).
- `data/processed/bluetrend_web_data.js` — Dữ liệu đã xử lý dùng trực tiếp cho `index.html`.
- `data/archive/` — Lưu các bản giao diện cũ.
- `src/bluetrend/analysis/build_web_data.py` — Pipeline Python tính Mann-Kendall, Sen's slope, trích xuất không gian và chấm điểm rủi ro.
- `metadata/`, `outputs/`, `docs/`, `config/` — Tài liệu kiểm kê, cấu hình và kết quả thống kê.

## Cách chạy

1. **Mở trực tiếp giao diện Web:** Mở tệp `index.html` bằng trình duyệt (Chrome/Edge).
2. **Cập nhật dữ liệu khi có input mới trong `data/incoming/`:**
   ```powershell
   .\.venv\Scripts\python.exe src\bluetrend\analysis\build_web_data.py
   ```
3. **Deploy nhanh:** Push `index.html` và `data/processed/bluetrend_web_data.js` lên GitHub và bật **GitHub Pages** (Branch `main` / `/ (root)`).
