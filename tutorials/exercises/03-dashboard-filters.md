# 🖥️ Bài tập 03. Dashboard có bộ lọc đồng bộ

[Bài trước](02-sql-analysis.md) · [Danh sách](README.md) · [Bài tiếp theo](04-visualization-sqlalchemy.md)

## 🎯 Đề bài

Xây dựng `app.py` cho phép người dùng khám phá doanh thu mà không viết SQL. Mọi chỉ số, biểu đồ, bảng và file tải về phải phản ánh cùng một bộ lọc.

Đọc trước [tutorial 03](../03-charts-ui.md). Thời gian dự kiến: 90 đến 120 phút.

## 📋 Yêu cầu bắt buộc

1. Đọc database đã tạo ở bài 01; không chạy INSERT mỗi khi Streamlit chạy lại script.
2. Tạo lựa chọn khu vực có Tất cả, Bắc, Trung, Nam, cùng bộ lọc tháng bắt đầu và kết thúc. Cho phép nhập khoảng ngoài dữ liệu để kiểm tra trạng thái rỗng.
3. Chặn khoảng tháng bắt đầu lớn hơn tháng kết thúc bằng thông báo dễ hiểu.
4. Hiển thị tổng doanh thu, số dòng và số khu vực của dữ liệu sau lọc.
5. Vẽ biểu đồ đường doanh thu theo tháng bằng Seaborn trên Matplotlib, tô màu theo khu vực; hiển thị bảng dữ liệu bên dưới.
6. Thêm tải CSV chứa đúng các dòng đang lọc. Có nhãn đơn vị doanh thu minh họa và mô tả phạm vi dữ liệu.
7. Khi không có dữ liệu, hiển thị thông báo, các chỉ số bằng 0 và không vẽ biểu đồ. Không để ứng dụng phát sinh exception.

## ✅ Kịch bản nghiệm thu

| Thao tác | Kết quả |
| :--- | :--- |
| Tất cả, từ tháng 1 đến tháng 6 năm 2026 | 18 dòng, doanh thu 15435, 3 khu vực |
| Bắc, từ tháng 2 đến tháng 4 năm 2026 | 3 dòng, doanh thu 1755, 1 khu vực |
| Nam, riêng tháng 6 năm 2026 | 1 dòng, doanh thu 1380, 1 khu vực |
| Tất cả, từ tháng 1 đến tháng 3 năm 2027 | Trạng thái rỗng, không có biểu đồ |
| Tháng bắt đầu sau tháng kết thúc | Thông báo khoảng tháng không hợp lệ |

Ở mỗi trường hợp có dữ liệu, tải CSV và so sánh số dòng, tổng doanh thu với giao diện. Với trường hợp rỗng, ẩn hoặc vô hiệu hóa nút tải và giải thích lựa chọn.

## 💡 Gợi ý

Dùng cùng một DataFrame đã lọc làm nguồn cho các thành phần. SQL cần lọc trước khi đọc dữ liệu. Dùng `st.metric`, `st.selectbox`, `st.pyplot`, `st.dataframe`, `st.download_button`. Với một điểm dữ liệu, marker giúp người dùng vẫn nhìn thấy kết quả.

## 📤 Sản phẩm nộp

`app.py`, lệnh chạy và ảnh hoặc video ngắn của năm kịch bản. Ghi lại quy tắc đồng bộ bộ lọc trong README bài nộp.

## 📝 Thang điểm

| Tiêu chí | Điểm |
| :--- | ---: |
| Bộ lọc SQL và kiểm tra khoảng tháng | 6 |
| Chỉ số, bảng và biểu đồ đồng bộ | 6 |
| CSV đúng dữ liệu, xử lý rỗng | 4 |
| Nhãn, bố cục và bằng chứng nghiệm thu | 4 |
