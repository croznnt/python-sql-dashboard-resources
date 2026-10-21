# 🎓 Tutorial Python, SQL và Dashboard

Bạn sẽ dựng một dashboard doanh thu có bộ lọc khu vực, tổng doanh thu, biểu đồ và bảng dữ liệu. Lộ trình dùng dữ liệu giả lập để có thể học mà không cần tài khoản cơ sở dữ liệu.

## 🧭 Lộ trình

| Bài | Nội dung | Kết quả |
| :--- | :--- | :--- |
| [01](01-setup.md) | Cài môi trường và chạy ứng dụng | Dashboard mở trên trình duyệt |
| [02](02-sql-pandas.md) | SQLite, SQL và pandas | Hiểu dữ liệu, bộ lọc và phép tổng hợp |
| [03](03-charts-ui.md) | Seaborn, Matplotlib và Streamlit | Hiểu toàn bộ mã giao diện và thêm biểu đồ |
| [04](04-external-databases.md) | SQLAlchemy, PostgreSQL và MySQL | Đọc dữ liệu từ server SQL |
| [05](05-testing-deployment.md) | Kiểm tra, xử lý lỗi và triển khai | Kiểm tra kết quả và vận hành ứng dụng |

## 🧑‍💻 Bài tập thực hành

[Bắt đầu bộ 5 bài thực hành](exercises/README.md). Các bài có CSV dùng chung, đề bài, hướng dẫn, dữ liệu và kết quả đối chiếu để tự kiểm tra. Lộ trình đi từ nạp dữ liệu tới SQL, dashboard, SQLAlchemy và kiểm thử bàn giao.

## 📁 Tệp thực hành

Mã hoàn chỉnh của bài SQLite nằm ở [app.py](../examples/streamlit_sqlite/app.py). Các đoạn SQLAlchemy trong bài 04 là bài thực hành riêng, lưu vào `external_query.py` ở thư mục gốc sau khi cấu hình server. Chúng chưa thay thế ứng dụng SQLite tự động.

## ✅ Tiêu chí hoàn thành

1. Chạy ứng dụng từ một môi trường ảo mới.
2. Giải thích được luồng SQL → DataFrame → biểu đồ → giao diện.
3. Chuyển bộ lọc từ Tất cả sang từng khu vực và đối chiếu tổng doanh thu.
4. Thêm được biểu đồ cột từ kết quả SQL tổng hợp.
5. Biết đặt thông tin kết nối ngoài mã nguồn và phân biệt demo với triển khai nhiều người dùng.

Tài liệu được đối chiếu với tài liệu chính thức ngày 15 tháng 10 năm 2026. Các liên kết API nằm trong từng bài. Phần server SQL yêu cầu cơ sở dữ liệu do bạn cấu hình riêng.
