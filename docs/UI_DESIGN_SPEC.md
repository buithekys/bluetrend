# UI & UX Design Specification — BlueTrend Streamlit App

> Tài liệu đặc tả thiết kế giao diện cho phiên bản Hackathon & mở rộng khi bổ sung dữ liệu mới (chuỗi 20+ năm, polygon lưu vực thật, SST, NetCDF có chiều thời gian).

---

## 1. Nguyên tắc thiết kế cốt lõi

1. **Insight-First (Tri thức trước, số liệu sau):** Mỗi màn hình mở đầu bằng **câu chuyện / nhận định rút ra từ dữ liệu** (ví dụ: *"Lưu vực X có lượng mưa tăng đáng kể trong 20 năm qua, đi kèm độ đục ven biển tăng"*), sau đó mới đến biểu đồ minh họa và cuối cùng là bảng số liệu kiểm chứng (có thể thu gọn trong `st.expander`).
2. **Mọi nút bấm (Button/Control) đều có chức năng cụ thể:** Không đặt widget trang trí. Mọi bộ lọc, nút chuyển lớp, nút tải xuống đều phải làm thay đổi trực tiếp bản đồ, biểu đồ hoặc xuất kết quả.
3. **Minh bạch khoa học:** Luôn hiển thị đơn vị trên trục biểu đồ, khoảng thời gian, nguồn NASA, và phân biệt rõ *"Chưa đủ bằng chứng thống kê"* với *"Không thay đổi"*.

---

## 2. Bố cục tổng thể & Điều hướng (Sidebar)

* **Header:** Logo/Tên `🌊 BlueTrend` + mô tả ngắn 1 dòng.
* **Bộ lọc toàn cục (Global Filters):**
  * `Chọn Nhóm nghiên cứu`: *Tất cả* / *Liên kết Đất liền – Biển (Land-to-Sea)* / *Chỉ Lưu vực sông* / *Chỉ Vùng biển*.
  * `Khoảng thời gian`: Slider chọn năm bắt đầu – kết thúc (mặc định toàn chuỗi).
* **Menu 4 Trang chính** (tinh gọn từ 5 trang thành 4 trang tập trung vào câu chuyện):
  1. **Overview & Interactive Map** (Bản đồ câu chuyện & Điểm nóng)
  2. **Basin-to-Sea Explorer** (Khám phá chuỗi thời gian & Mùa vụ)
  3. **Cross-Basin Comparison** (So sánh & Xếp hạng có kiểm soát)
  4. **Methodology & Data Provenance** (Nguồn NASA & Giới hạn khoa học)

---

## 3. Thiết kế chi tiết từng trang & Chức năng từng Button

### Trang 1: Overview & Interactive Map
* **Mục tiêu:** Trả lời ngay câu hỏi *"Đâu là điểm nóng đang thay đổi rõ rệt nhất?"* trong 5 giây đầu.
* **Bố cục:**
  * **Hàng 1 — Insight Banner (3 thẻ KPI):**
    * Số vùng có xu hướng tăng có ý nghĩa ($p < 0.05$).
    * Vùng biến động mạnh nhất (tên + tốc độ thay đổi).
    * Mức độ sẵn sàng dữ liệu (ví dụ: Polygon thật vs Bounding box).
  * **Hàng 2 — Bản đồ tương tác (70% chiều rộng) + Bảng tóm tắt điểm nóng (30%):**
    * **Radio/Toggle lớp bản đồ:** `Xu hướng Mưa (GPM)` | `Xu hướng Độ đục Kd490 (MODIS)` | `Nhiệt độ mặt biển SST (MODIS)`.
    * **Checkbox `Hiện lớp phủ Raster nền`:** Bật/tắt lớp ảnh màu trung bình từ `.nc`/`.tif` kèm thanh chú giải màu (Colorbar).
    * **Click vào Polygon trên bản đồ:** Hiển thị Popup gồm tên vùng, nhận định 1 câu, `Sen's slope`, `p-value`.
  * **Hàng 3 — Nút hành động:**
    * `Button: Tải báo cáo tóm tắt (CSV)` — Xuất bảng kết quả kiểm định hiện tại.

### Trang 2: Basin-to-Sea Explorer
* **Mục tiêu:** Phân tích sâu từng lưu vực/vùng biển và **mối liên kết Đất liền – Biển**.
* **Bố cục:**
  * **Thanh chọn:** `Selectbox: Chọn Lưu vực / Vùng biển` + `Toggle: So sánh cặp Đất liền – Biển tương ứng` (ví dụ: *Mekong ↔ Vịnh Thái Lan*).
  * **Khối Nhận định tự động:** Hộp màu xanh/vàng tóm tắt xu hướng, độ tin cậy và cảnh báo mùa vụ.
  * **2 Biểu đồ song song:**
    * **Trái:** Chuỗi thời gian (Plotly) kèm đường xu hướng `Sen's slope` / `OLS` và nút `Checkbox: Hiện đường trung bình trượt 12 tháng` (để thấy xu hướng dài hạn tách khỏi dao động mùa).
    * **Phải:** **Heatmap Tháng × Năm** (Trục X: Năm, Trục Y: Tháng 1–12) giúp nhận diện trực quan tháng bất thường và sự dịch chuyển mùa mưa/khô.
  * **Thu gọn (`st.expander`):** Bảng dữ liệu thô & nút `Download CSV`.

### Trang 3: Cross-Basin Comparison
* **Mục tiêu:** So sánh công bằng giữa các vùng có cùng biến, cùng đơn vị và cùng khoảng thời gian.
* **Bố cục:**
  * `Selectbox: Chọn Biến so sánh` (`Precipitation`, `Kd490`, `SST`).
  * `Toggle: Chỉ hiển thị các vùng có ý nghĩa thống kê (p < 0.05)`.
  * **Biểu đồ cột ngang (Horizontal Bar Chart):** Sắp xếp theo `Sen's slope`, tô màu theo `significance` (đỏ/xanh cho có ý nghĩa, xám cho chưa có ý nghĩa).
  * **Lưu ý tự động:** Ghi rõ vùng nào bị loại khỏi phép so sánh (nếu khác đơn vị/thiếu dữ liệu).

### Trang 4: Methodology & Data Provenance
* **Mục tiêu:** Tạo sự tin cậy tuyệt đối trước ban giám khảo Hackathon.
* **Nội dung:**
  * Bảng trích dẫn chuẩn các bộ dữ liệu NASA (`GPM_3IMERGM_07`, `MODISA_L3m_KD`, `MODISA_L3m_SST`).
  * Giải thích ngắn gọn phương pháp Mann-Kendall & Sen's slope (tại sao dùng phương pháp phi tham số cho dữ liệu môi trường).
  * Danh sách các giới hạn hiện tại (ví dụ: chuỗi ngắn, chưa tách mùa vụ, bounding box) và nút `Button: Xem Data Catalog đầy đủ`.
