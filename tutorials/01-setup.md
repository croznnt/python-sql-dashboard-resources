# 🚀 Bài 01. Cài đặt và chạy dashboard

[Lộ trình](README.md) · [Bài tiếp theo](02-sql-pandas.md)

## 1. Chuẩn bị

Cài Python 3.10 trở lên và Git. Python 3.11 hoặc 3.12 là lựa chọn thực hành phù hợp nếu máy chưa có Python. Kiểm tra bằng `python --version` và `git --version`. Nếu Windows chỉ nhận `py`, thay lệnh `python` đầu tiên bằng `py`.

## 2. Lấy đúng nhánh

```powershell
git clone --branch codex/tutorial https://github.com/croznnt/python-sql-dashboard-resources.git
cd python-sql-dashboard-resources
git branch --show-current
```

Kết quả lệnh cuối phải là `codex/tutorial`. Nếu đã clone repo, vào thư mục đó rồi chạy `git fetch origin` và `git switch codex/tutorial`. Lưu các thay đổi cá nhân trước khi đổi nhánh.

## 3. Tạo môi trường ảo

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m streamlit run examples/streamlit_sqlite/app.py
```

macOS hoặc Linux:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run examples/streamlit_sqlite/app.py
```

Không cần activate môi trường vì lệnh đã gọi trực tiếp Python bên trong `.venv`. Giữ terminal đang chạy, mở địa chỉ Local URL mà Streamlit in ra, thường là `http://localhost:8501`. Nhấn Ctrl+C trong terminal để dừng.

## 4. Xác nhận kết quả

Bạn thấy tiêu đề Doanh thu từ SQLite, bộ lọc khu vực, tổng doanh thu, biểu đồ đường và bảng dữ liệu. Chọn Tất cả sẽ có 18 dòng. Chọn một khu vực sẽ có 6 dòng.

Ví dụ không cần file CSV, mật khẩu hoặc dịch vụ SQL. Mỗi lần tương tác, Streamlit chạy lại script và tạo lại SQLite trong bộ nhớ. Dữ liệu này không được lưu sau khi đóng kết nối.

## 5. Vai trò các thư viện

| Công cụ | Vai trò |
| :--- | :--- |
| sqlite3 | Tạo cơ sở dữ liệu demo, có sẵn trong Python |
| pandas | Đọc kết quả SQL thành DataFrame |
| Seaborn | Vẽ biểu đồ thống kê từ DataFrame |
| Matplotlib | Quản lý Figure, trục và xuất hình |
| Streamlit | Tạo giao diện và phản hồi thao tác bộ lọc |

Nếu thiếu thư viện, chạy lại lệnh cài đặt bằng chính Python trong `.venv`. Không cài gói tên `sqlite3` qua pip.

## 🧑‍💻 Thực hành sau bài học

[Làm bài tập 01](exercises/01-environment-data.md), xem yêu cầu, kết quả cần đạt và hướng dẫn thực hành.
