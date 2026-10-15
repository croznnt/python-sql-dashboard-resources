# ✅ Bài 05. Kiểm tra, xử lý lỗi và triển khai

[Bài trước](04-external-databases.md) · [Lộ trình](README.md)

## 1. Kiểm tra trước khi chia sẻ

Chạy từ thư mục gốc:

```powershell
.venv\Scripts\python -m compileall examples
.venv\Scripts\python -m pip check
.venv\Scripts\python -m streamlit run examples/streamlit_sqlite/app.py
```

`compileall` phát hiện lỗi cú pháp; `pip check` phát hiện xung đột phụ thuộc đã cài. Hai lệnh này không chứng minh kết quả nghiệp vụ đúng. Mở giao diện để đối chiếu bảng kết quả bài 02, thử đủ ba khu vực và Tất cả.

Nếu thêm nút tải CSV, xác nhận file xuất phản ánh bộ lọc. Nếu chuyển sang server SQL, thử trường hợp bảng rỗng, thông tin kết nối sai và mất kết nối. Thông báo cho người dùng cần dễ hiểu, còn chi tiết lỗi nên được ghi vào log được kiểm soát truy cập.

## 2. Lỗi thường gặp

| Hiện tượng | Nguyên nhân cần kiểm tra | Cách xử lý |
| :--- | :--- | :--- |
| ModuleNotFoundError | Dùng sai Python hoặc chưa cài đủ gói | Cài requirements bằng Python trong `.venv` |
| Không tìm thấy app.py | Terminal ở sai thư mục | Vào thư mục gốc repo rồi chạy lại |
| Port đã được dùng | Có server khác ở port 8501 | Thêm `--server.port 8502` vào lệnh chạy |
| no such table: sales | SQLite trong bộ nhớ đã đổi kết nối | Khởi tạo và đọc trên cùng kết nối |
| Tổng doanh thu sai | Dữ liệu bị nạp lặp hoặc bộ lọc khác | Đối chiếu số dòng, WHERE và GROUP BY |
| Biểu đồ rỗng | Truy vấn rỗng hoặc kiểu cột không đúng | Kiểm tra `data.empty` và `data.dtypes` |
| Font tiếng Việt lỗi | Font trên máy thiếu ký tự | Cài font hỗ trợ tiếng Việt và cấu hình Matplotlib |
| Kết nối server thất bại | Host, port, driver, quyền hoặc TLS | Kiểm tra từng cấu hình bằng script bài 04 |

## 3. Chạy headless

```powershell
.venv\Scripts\python -m streamlit run examples/streamlit_sqlite/app.py --server.headless true
```

Lệnh này không tự mở trình duyệt. Nó chưa cung cấp tên miền, HTTPS hoặc đăng nhập. Với triển khai nhiều người dùng, cần nền tảng hosting, cấu hình mạng, kiểm soát truy cập và xem xét việc Matplotlib có thể gặp vấn đề khi chạy đồng thời nhiều luồng.

## 4. Triển khai bằng Streamlit Community Cloud

1. Đẩy mã lên GitHub và mở dịch vụ [Streamlit Community Cloud](https://streamlit.io/cloud).
2. Kết nối tài khoản GitHub theo hướng dẫn của dịch vụ.
3. Chọn repo `croznnt/python-sql-dashboard-resources`, nhánh `codex/tutorial`, entrypoint `examples/streamlit_sqlite/app.py`.
4. Chọn Python tương thích với requirements và triển khai. Xem log cài phụ thuộc nếu build lỗi.
5. Thử lại bộ lọc và đối chiếu số liệu. Demo SQLite không cần secrets.

Nếu dùng server SQL, thêm driver vào requirements, cấu hình secrets của nền tảng và đọc chúng bằng cơ chế thích hợp. Không giả định secrets luôn tự trở thành biến môi trường. Server database phải cho phép kết nối từ môi trường hosting; cấu hình theo hướng dẫn nhà cung cấp.

## 5. Ghi lại môi trường

Sau khi đã chạy thành công, xuất snapshot phụ thuộc từ môi trường ảo:

```powershell
.venv\Scripts\python -m pip freeze > requirements-tested.txt
```

Lưu thêm phiên bản Python và hệ điều hành cùng kết quả kiểm tra. Snapshot phản ánh môi trường hiện tại, không thay thế kiểm tra trên máy hoặc nền tảng khác.

## 🧪 Bài tập hoàn thiện

1. Thêm bộ lọc tháng, tính tổng trong SQL và đối chiếu bằng tay.
2. Thêm biểu đồ cột theo khu vực cùng tải CSV theo bài 03.
3. Tách hàm truy vấn khỏi phần giao diện để có thể kiểm tra dữ liệu độc lập.
4. Thay SQLite bằng database thực hành ở bài 04, giữ kết quả biểu đồ nhất quán với truy vấn server.

## 📖 Nguồn

1. [Triển khai Streamlit Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app).
2. [Secrets trong Streamlit](https://docs.streamlit.io/develop/concepts/connections/secrets-management).
3. [Lưu ý Matplotlib trong Streamlit](https://docs.streamlit.io/develop/api-reference/charts/st.pyplot).

## 🧑‍💻 Thực hành sau bài học

[Làm bài tập 05](exercises/05-final-project.md), xem yêu cầu, kết quả cần đạt và tiêu chí chấm.
