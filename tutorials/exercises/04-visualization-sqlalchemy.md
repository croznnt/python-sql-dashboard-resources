# 📈 Bài tập 04. So sánh khu vực và tách lớp SQLAlchemy

[Bài trước](03-dashboard-filters.md) · [Danh sách](README.md) · [Bài tiếp theo](05-final-project.md)

## 🎯 Đề bài

Nâng cấp dashboard bằng biểu đồ so sánh và một lớp dữ liệu có thể tái sử dụng. Bài bắt buộc dùng SQLAlchemy với SQLite; chuyển sang PostgreSQL hoặc MySQL là phần mở rộng tùy chọn.

Đọc trước [tutorial 03](../03-charts-ui.md) và [tutorial 04](../04-external-databases.md). Thời gian dự kiến: 90 đến 120 phút.

## 📋 Yêu cầu bắt buộc

1. Cài `SQLAlchemy>=2,<3` trong môi trường ảo và ghi phụ thuộc vào requirements của bài nộp.
2. Tạo `database.py` có hàm đọc chi tiết và hàm tổng hợp theo khu vực, nhận khu vực cùng tháng bắt đầu, tháng kết thúc. Không import Streamlit trong module dữ liệu.
3. Dùng `create_engine`, `text` và tham số có tên như `:region`. Đọc URL kết nối từ biến môi trường hoặc cấu hình ngoài mã nguồn. Với SQLite, xác định đường dẫn file rõ ràng, tránh vô tình tạo database rỗng ở thư mục làm việc khác.
4. Thay lớp sqlite3 trong dashboard bằng module mới, giữ nguyên kết quả bộ lọc bài 03. Đóng kết nối bằng context manager.
5. Thêm biểu đồ cột tổng doanh thu theo khu vực, sắp xếp giảm dần, nhãn trục rõ và nhãn giá trị. Cột, đường, bảng và metric phải dùng cùng bộ lọc.
6. Viết đoạn nhận xét ngắn về doanh thu và phân biệt tỷ trọng doanh thu với tỷ trọng số repo trong biểu đồ framework của repo học liệu.

## ✅ Kết quả đối chiếu

Khi chọn Tất cả và toàn bộ sáu tháng, biểu đồ cột có thứ tự Nam 6405, Trung 5145, Bắc 3885. Khi chỉ chọn Bắc từ tháng 2 đến tháng 4, có một cột 1755. Trường hợp rỗng không vẽ cả hai biểu đồ.

Gọi trực tiếp hàm dữ liệu trong Python mà không chạy Streamlit vẫn nhận được kết quả đúng. Thay đổi thư mục làm việc khi gọi ứng dụng không được làm mất bảng do trỏ nhầm file SQLite.

## 🌱 Mở rộng tùy chọn

Nạp cùng CSV vào database PostgreSQL hoặc MySQL riêng. Cài driver phù hợp, đổi URL cấu hình và chứng minh kết quả không đổi. Không dùng bộ dữ liệu 3 dòng trong ví dụ tutorial để đối chiếu các tổng của bài tập này. Không nộp mật khẩu hoặc URL chứa mật khẩu thật.

## 💡 Gợi ý

Tách vòng đời engine khỏi từng truy vấn. Không chia sẻ một kết nối đang sử dụng giữa các phiên. Với bài thực hành cục bộ, ưu tiên cấu trúc rõ ràng và kết quả đúng trước khi thêm cache. Nếu cache, phải giải thích thời điểm dữ liệu được làm mới.

## 📤 Sản phẩm nộp

`database.py`, app đã cập nhật, requirements bài nộp, cấu hình mẫu không có bí mật và bảng đối chiếu trước, sau khi chuyển SQLAlchemy.

## 📝 Thang điểm

| Tiêu chí | Điểm |
| :--- | ---: |
| Module dữ liệu tách biệt và cấu hình kết nối | 6 |
| SQLAlchemy, tham số và quản lý kết nối | 6 |
| Biểu đồ cột đúng, đồng bộ bộ lọc | 4 |
| Đối chiếu kết quả và nhận xét | 4 |
