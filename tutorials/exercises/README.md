# 🧑‍💻 Bộ 5 bài thực hành

[Về tutorial](../README.md)

## 🎯 Mục tiêu

Hoàn thành một dashboard doanh thu từ dữ liệu CSV, lưu vào SQL, truy vấn bằng tham số, trực quan hóa và kiểm tra kết quả. Làm lần lượt vì sản phẩm bài trước là đầu vào bài sau. Không cần tài khoản dịch vụ trả phí; bài SQLAlchemy có thể dùng SQLite ngay trên máy.

| Bài | Chủ đề | Tutorial liên quan | Thời gian dự kiến |
| :--- | :--- | :--- | :--- |
| [01](01-environment-data.md) | Môi trường và dữ liệu | Bài 01 | 45 đến 60 phút |
| [02](02-sql-analysis.md) | Truy vấn và kiểm tra doanh thu | Bài 02 | 60 đến 90 phút |
| [03](03-dashboard-filters.md) | Dashboard và bộ lọc | Bài 02, 03 | 90 đến 120 phút |
| [04](04-visualization-sqlalchemy.md) | Biểu đồ và SQLAlchemy | Bài 03, 04 | 90 đến 120 phút |
| [05](05-final-project.md) | Kiểm thử và bàn giao | Bài 05 | 90 đến 120 phút |

## 📦 Dữ liệu chung

[sales.csv](data/sales.csv) gồm 18 dòng doanh thu giả lập, từ tháng 1 đến tháng 6 năm 2026, thuộc Bắc, Trung và Nam. Mỗi cặp tháng và khu vực có một dòng. `revenue` là số nguyên theo đơn vị minh họa, không phải dữ liệu kinh doanh thật.

| Cột | Kiểu mong đợi | Ý nghĩa |
| :--- | :--- | :--- |
| month | TEXT | Chuỗi năm tháng, ví dụ 2026-01 |
| region | TEXT | Bắc, Trung hoặc Nam |
| revenue | INTEGER | Doanh thu không âm |

Giữ nguyên CSV gốc để đối chiếu. Bài xử lý dữ liệu rỗng dùng bộ lọc tháng ngoài phạm vi, không yêu cầu sửa dữ liệu.

## 📁 Tổ chức thư mục thực hành

Tạo thư mục `practice/<ten-cua-ban>/` trong bản clone hoặc fork cá nhân. Bài 01 tạo `load_data.py`, bài 02 tạo `queries.sql` và `analysis.py`, bài 03 tạo `app.py`, bài 04 tạo `database.py`, bài 05 thêm `tests/` và `REPORT.md`. Có thể dùng cấu trúc khác nếu hướng dẫn chạy giải thích rõ.

Mỗi bài nên lưu mã nguồn, hướng dẫn chạy và kết quả kiểm tra để tự đối chiếu. Không đưa `.venv`, mật khẩu hoặc database cá nhân lên GitHub. Dữ liệu demo có thể tái tạo từ CSV; không cần lưu file SQLite trong repo.

Các con số đối chiếu trong đề dùng bộ CSV chung. Bài 04 của tutorial có một bộ dữ liệu server 3 dòng khác; khi làm bộ bài tập này, luôn nạp CSV 18 dòng để giữ kết quả nhất quán.
