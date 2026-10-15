# 🔎 Bài tập 02. Phân tích doanh thu bằng SQL

[Bài trước](01-environment-data.md) · [Danh sách](README.md) · [Bài tiếp theo](03-dashboard-filters.md)

## 🎯 Đề bài

Dùng database 18 dòng từ bài 01 để viết báo cáo doanh thu. SQL thực hiện lọc và tổng hợp; pandas chỉ nhận kết quả và trình bày bảng.

Đọc trước [tutorial 02](../02-sql-pandas.md). Thời gian dự kiến: 60 đến 90 phút.

## 📋 Yêu cầu bắt buộc

1. Trong `queries.sql`, viết truy vấn tổng doanh thu và số dòng toàn bộ dữ liệu.
2. Tính doanh thu theo khu vực, sắp xếp giảm dần. Tính doanh thu theo tháng, sắp xếp tăng dần theo tháng.
3. Viết truy vấn lọc theo khu vực và khoảng tháng, bao gồm cả hai đầu mút. Trong `analysis.py`, nhận ba tham số rồi gọi truy vấn qua placeholder, không ghép giá trị trực tiếp vào SQL.
4. Tính tỷ trọng doanh thu từng khu vực trên toàn bộ dữ liệu. Giữ số gốc để tính, chỉ làm tròn khi hiển thị.
5. Với bộ lọc không có dữ liệu, báo số dòng bằng 0 và tổng hiển thị bằng 0; giải thích vì sao `SUM` có thể trả NULL.
6. Xuất kết quả tổng hợp khu vực thành CSV, không kèm cột index.

## ✅ Kết quả đối chiếu

| Khu vực | Doanh thu |
| :--- | ---: |
| Nam | 6405 |
| Trung | 5145 |
| Bắc | 3885 |

Tổng ba khu vực là 15435. Tổng tháng 1 là 1635, tháng 6 là 3510. Bộ lọc Bắc từ `2026-02` đến `2026-04` có 3 dòng và doanh thu 1755. Khoảng `2027-01` đến `2027-03` trả 0 dòng.

Tổng tỷ trọng trước làm tròn phải bằng 100% trong sai số số thực hợp lý. Trình bày tỷ trọng với hai chữ số thập phân và lưu ý tổng sau làm tròn có thể khác 100% một lượng nhỏ.

## 💡 Gợi ý

Xem `GROUP BY`, `ORDER BY`, `SUM`, `COUNT` và `COALESCE`. Với SQLite, placeholder giá trị là `?`. Các chuỗi tháng dạng `YYYY-MM` có thứ tự thời gian phù hợp để lọc trong bộ dữ liệu này.

## 📤 Sản phẩm nộp

`queries.sql`, `analysis.py`, CSV tổng hợp và kết quả chạy các trường hợp đối chiếu. Chỉ rõ truy vấn nào chạy trên database và phần nào do Python xử lý.

## 📝 Thang điểm

| Tiêu chí | Điểm |
| :--- | ---: |
| Tổng hợp SQL đúng và đúng thứ tự | 6 |
| Bộ lọc có tham số và đúng hai đầu mút | 6 |
| Tỷ trọng, dữ liệu rỗng và xuất CSV | 4 |
| Bằng chứng đối chiếu và giải thích | 4 |
