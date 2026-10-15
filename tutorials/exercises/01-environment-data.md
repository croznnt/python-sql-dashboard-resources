# 🧪 Bài tập 01. Chuẩn bị môi trường và nạp dữ liệu

[Danh sách bài tập](README.md) · [Bài tiếp theo](02-sql-analysis.md)

## 🎯 Đề bài

Bạn được giao chuẩn bị dữ liệu cho dashboard doanh thu. Từ [sales.csv](data/sales.csv), xây dựng script tạo cơ sở dữ liệu SQLite có thể chạy lại nhiều lần mà không nhân đôi dữ liệu.

Đọc trước [tutorial 01](../01-setup.md). Thời gian dự kiến: 45 đến 60 phút.

## 📋 Yêu cầu bắt buộc

1. Clone đúng nhánh `codex/tutorial`, tạo môi trường ảo và cài `requirements.txt`.
2. Tạo `load_data.py` đọc CSV với UTF-8, kiểm tra tên cột, giá trị trống và kiểu doanh thu.
3. Tạo bảng `sales` có ba cột theo mô tả dữ liệu. Cặp `(month, region)` phải duy nhất và doanh thu không âm.
4. Nạp dữ liệu bằng tham số SQL. Khi chạy lại với cùng CSV, bảng vẫn có đúng 18 dòng. Chọn cơ chế thay thế dữ liệu demo hoặc cập nhật theo khóa, rồi giải thích lựa chọn.
5. Xác định đường dẫn CSV theo vị trí script hoặc đối số dòng lệnh, không viết đường dẫn tuyệt đối chỉ có trên máy của bạn.
6. In số dòng, số khu vực, tháng đầu, tháng cuối và tổng doanh thu sau khi nạp.

## ✅ Kết quả đối chiếu

| Chỉ số | Kết quả |
| :--- | ---: |
| Số dòng | 18 |
| Số khu vực | 3 |
| Tháng đầu | 2026-01 |
| Tháng cuối | 2026-06 |
| Tổng doanh thu | 15435 |

Chạy script hai lần và lưu bằng chứng số dòng không tăng. Trên bản sao CSV, thử một doanh thu âm hoặc cặp khóa trùng và mô tả cách chương trình phản hồi; không chỉnh CSV gốc.

## 💡 Gợi ý

Dùng `pathlib.Path`, `sqlite3`, `csv` hoặc pandas. Tách bước kiểm tra đầu vào khỏi bước ghi database. Nếu cần nhiều lệnh ghi, thực hiện trong transaction để tránh dữ liệu nạp dở khi có lỗi.

## 📤 Sản phẩm nộp

`load_data.py`, hướng dẫn chạy từ thư mục gốc và kết quả của hai lần chạy liên tiếp. Giải thích ngắn khóa duy nhất giúp tránh lỗi gì.

## 📝 Thang điểm

| Tiêu chí | Điểm |
| :--- | ---: |
| Môi trường và hướng dẫn chạy tái tạo được | 4 |
| Kiểm tra CSV và thiết kế ràng buộc | 6 |
| Nạp bằng tham số, chạy lại không trùng | 6 |
| Kết quả đối chiếu và giải thích | 4 |
