# 🗄️ Bài 02. Từ SQL tới pandas

[Bài trước](01-setup.md) · [Lộ trình](README.md) · [Bài tiếp theo](03-charts-ui.md)

## 1. Hiểu dữ liệu

Bảng `sales` gồm `month` dạng chuỗi năm tháng, `region` là khu vực và `revenue` là doanh thu minh họa. Mỗi tháng có ba khu vực, từ tháng 1 đến tháng 6 năm 2026. Chuỗi tháng luôn có hai chữ số nên thứ tự chuỗi cũng là thứ tự tháng trong bộ dữ liệu này.

Trong dữ liệu tài chính thật, chọn kiểu số và đơn vị tiền tệ theo yêu cầu nghiệp vụ. `REAL` trong SQLite demo không phải thiết kế kế toán chính xác tuyệt đối.

## 2. Tạo bảng và dữ liệu

Đọc đoạn `CREATE TABLE` và `executemany` trong [mã nguồn](../examples/streamlit_sqlite/app.py). Công thức dữ liệu là `month * 125 + offset * 210`, trong đó Bắc, Trung, Nam có offset lần lượt 1, 2, 3.

`executemany` gửi danh sách bộ giá trị vào cùng một câu INSERT. Dấu `?` là chỗ giữ tham số cho sqlite3. Không ghép giá trị người dùng vào câu SQL bằng f-string.

## 3. Lọc và đọc dữ liệu

```python
query = "SELECT month, region, revenue FROM sales WHERE region = ? ORDER BY month"
data = pd.read_sql_query(query, connection, params=("Bắc",))
```

Đoạn trên chạy bên trong khối `try` của ứng dụng, trước khi đóng kết nối. Tuple một phần tử phải có dấu phẩy. pandas trả về DataFrame có tên cột tương ứng SELECT. Dùng `data.head()`, `data.dtypes` và `data.shape` để khảo sát.

`finally` đóng kết nối kể cả khi truy vấn thất bại. Vì demo dùng `:memory:`, kết nối khác sẽ không nhìn thấy bảng này. Nếu chuyển sang file SQLite, cần thiết kế phần khởi tạo riêng để tránh tạo bảng trùng hoặc nạp lặp dữ liệu.

## 4. Tổng hợp ngay trong SQL

Thay phần đọc dữ liệu, vẫn bên trong khối `try`, bằng truy vấn sau để thực hành:

```python
totals = pd.read_sql_query(
    "SELECT region, SUM(revenue) AS total_revenue "
    "FROM sales GROUP BY region ORDER BY total_revenue DESC",
    connection,
)
```

`GROUP BY` gom các dòng theo khu vực. `SUM` tính doanh thu từng nhóm. Alias `total_revenue` là tên cột để dùng trong biểu đồ bài tiếp theo. Truy vấn này tổng hợp tất cả khu vực, độc lập bộ lọc hiện tại.

## 5. Đối chiếu kết quả

| Bộ lọc | Số dòng | Tổng doanh thu |
| :--- | ---: | ---: |
| Tất cả | 18 | 15435 |
| Bắc | 6 | 3885 |
| Trung | 6 | 5145 |
| Nam | 6 | 6405 |

Tổng ba khu vực phải bằng tổng Tất cả. Đổi một giá trị dữ liệu và kiểm tra tổng có thay đổi đúng như tính tay. Khi SQL trả về rỗng, hiển thị thông báo và bỏ qua phần vẽ biểu đồ.

## 📖 Nguồn

1. [sqlite3 trong Python](https://docs.python.org/3/library/sqlite3.html).
2. [pandas.read_sql_query](https://pandas.pydata.org/docs/reference/api/pandas.read_sql_query.html).

## 🧑‍💻 Thực hành sau bài học

[Làm bài tập 02](exercises/02-sql-analysis.md), xem yêu cầu, kết quả cần đạt và hướng dẫn thực hành.
