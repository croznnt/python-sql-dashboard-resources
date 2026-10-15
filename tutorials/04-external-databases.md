# 🔌 Bài 04. PostgreSQL và MySQL với SQLAlchemy

[Bài trước](03-charts-ui.md) · [Lộ trình](README.md) · [Bài tiếp theo](05-testing-deployment.md)

## 1. Chuẩn bị server và bảng

Phần này cần server PostgreSQL hoặc MySQL đang chạy, một database riêng để thực hành và tài khoản được cấp quyền trong database đó. Thay các giá trị placeholder bằng cấu hình của bạn. Không chạy lệnh tạo dữ liệu demo vào bảng sản xuất.

Chạy SQL sau bằng công cụ SQL của server, trong database thực hành mới chưa có bảng `sales`:

```sql
CREATE TABLE sales (
    month VARCHAR(7) NOT NULL,
    region VARCHAR(20) NOT NULL,
    revenue DECIMAL(14, 2) NOT NULL
);
INSERT INTO sales (month, region, revenue) VALUES
('2026-01', 'Bắc', 335),
('2026-01', 'Trung', 545),
('2026-01', 'Nam', 755);
```

Đảm bảo database MySQL dùng bộ ký tự hỗ trợ tiếng Việt như utf8mb4. Bộ dữ liệu server này có 3 dòng, khác bộ demo SQLite có 18 dòng.

## 2. Cài driver

Windows, chọn một loại database:

```powershell
.venv\Scripts\python -m pip install "SQLAlchemy>=2,<3" "psycopg[binary]>=3,<4"
```

Hoặc MySQL:

```powershell
.venv\Scripts\python -m pip install "SQLAlchemy>=2,<3" "PyMySQL>=1,<2"
```

Trên macOS hoặc Linux, thay đường dẫn Python bằng `.venv/bin/python`. Các gói này là phần mở rộng, không bắt buộc cho demo SQLite.

## 3. Cấu hình kết nối

Dùng biến môi trường cho host, tên database, user và mật khẩu. Trên PowerShell:

```powershell
$env:DB_DRIVER = 'postgresql+psycopg'
$env:DB_HOST = 'localhost'
$env:DB_PORT = '5432'
$env:DB_NAME = 'dashboard_demo'
$env:DB_USER = 'dashboard_reader'
$env:DB_PASSWORD = Read-Host 'Mật khẩu database' -MaskInput
```

`-MaskInput` yêu cầu PowerShell 7.1 trở lên. Nếu dùng Windows PowerShell cũ, cấu hình bí mật qua cơ chế secrets của môi trường chạy. Không viết mật khẩu thật vào script hoặc commit lên GitHub.

Với MySQL, đổi driver thành `mysql+pymysql` và port thành `3306`. Trên bash hoặc zsh, có thể dùng `export DB_DRIVER='postgresql+psycopg'`, tương tự cho các biến còn lại; nhập mật khẩu qua `read -s DB_PASSWORD` rồi `export DB_PASSWORD`.

## 4. Tạo script truy vấn hoàn chỉnh

Lưu đoạn dưới thành `external_query.py` ở thư mục gốc. `URL.create` xử lý ký tự đặc biệt trong mật khẩu mà không cần tự ghép URL:

```python
import os

import pandas as pd
from sqlalchemy import URL, create_engine, text

url = URL.create(
    drivername=os.environ["DB_DRIVER"],
    username=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    host=os.environ["DB_HOST"],
    port=int(os.environ["DB_PORT"]),
    database=os.environ["DB_NAME"],
)
engine = create_engine(url, pool_pre_ping=True)
try:
    with engine.connect() as connection:
        data = pd.read_sql_query(
            text("SELECT month, region, revenue FROM sales "
                 "WHERE region = :region ORDER BY month LIMIT 1000"),
            connection,
            params={"region": "Bắc"},
        )
    print(data.to_string(index=False))
finally:
    engine.dispose()
```

Chạy `.venv\Scripts\python external_query.py`. Với dữ liệu trên, kết quả Bắc có một dòng doanh thu 335. Không dùng dấu `?` của sqlite3 trong câu SQLAlchemy này; `text` dùng tham số có tên.

## 5. Ghép vào dashboard

1. Thêm import `os`, `URL`, `create_engine`, `text` vào app.
2. Thay toàn bộ khối tạo SQLite và nạp dữ liệu bằng cấu hình engine cùng truy vấn server. Giữ kết quả tên `data` để phần biểu đồ tiếp tục dùng được.
3. Với lựa chọn Tất cả, bỏ WHERE và không truyền tham số khu vực. Với từng khu vực, dùng `params={"region": region}`. Giữ ORDER BY và LIMIT sau WHERE.
4. Giữ phần bộ lọc, metric, biểu đồ và bảng. Không giữ INSERT demo trong dashboard đọc dữ liệu thật.
5. Khi vận hành, tái sử dụng engine qua cơ chế quản lý tài nguyên của Streamlit và rà soát cấu hình pool. Không chia sẻ một kết nối đang dùng giữa các phiên.

Tài khoản chạy dashboard chỉ cần SELECT trên các bảng được phép đọc. Quản trị viên cấp quyền phù hợp; tài khoản tạo bảng demo có thể có quyền khác. Với kết nối qua mạng, cấu hình TLS theo nhà cung cấp và driver.

## 📖 Nguồn

1. [SQLAlchemy Engine và URL](https://docs.sqlalchemy.org/en/20/core/engines.html).
2. [SQLAlchemy kết nối và tham số](https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html).
3. [Streamlit kết nối dữ liệu](https://docs.streamlit.io/develop/concepts/connections).

## 🧑‍💻 Thực hành sau bài học

[Làm bài tập 04](exercises/04-visualization-sqlalchemy.md), xem yêu cầu, kết quả cần đạt và hướng dẫn thực hành.
