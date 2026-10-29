# Thực hành NumPy với dữ liệu kho

Bộ thực hành hướng dẫn đọc dữ liệu SQLite, xử lý mảng NumPy và tạo báo cáo trên máy cá nhân. Tình huống xuyên suốt là phân tích giờ hoạt động, lập kịch bản thêm giờ và so sánh thứ tự ưu tiên theo trọng số. NumPy thực hiện tính toán, sqlite3 truy vấn và csv lưu kết quả.

## Lộ trình thực hành

| Bài | Nội dung | Kết quả cần đạt |
| :--- | :--- | :--- |
| [1. Đọc SQL và tạo mảng](bai-thuc-hanh/01-doc-du-lieu-va-mang.md) | Căn dữ liệu theo mã, lọc Boolean, đếm trạng thái | Hiểu quan hệ giữa vị trí mảng, mã và giá trị |
| [2. Broadcasting và kịch bản](bai-thuc-hanh/02-broadcasting-va-kich-ban.md) | Ma trận nhiều kịch bản, axis, np.select | Giải thích kết quả theo dòng và cột |
| [3. Chuẩn hóa và xếp hạng](bai-thuc-hanh/03-chuan-hoa-va-xep-hang.md) | Chuẩn hóa, @, argsort, đổi trọng số, CSV | So sánh thứ tự và kiểm chứng kết quả |

Ba bài nối tiếp nhau trong [luong_numpy.py](luong_numpy.py). Mỗi bài có mục tiêu, yêu cầu, code minh họa, giải thích tham số, kết quả đối chiếu và phần tự vận dụng. Đọc theo thứ tự để hiểu các biến được tạo ở đâu.

## Tệp và dữ liệu

1. [luong_numpy.py](luong_numpy.py): chương trình hoàn chỉnh.
2. [requirements.txt](requirements.txt): thư viện cần cài.
3. [Warehouse_Automation.db](Warehouse_Automation.db): database kho mô phỏng do người dùng cung cấp.
4. [ket_qua_mau](ket_qua_mau/): bốn CSV để đối chiếu. Chương trình tạo kết quả mới trong `ket_qua_numpy`.

Database có bốn thiết bị và hai bản ghi cảnh báo. Bài dùng ThietBi và truy vết CanhBao qua DuLieuCamBien, CamBien. Dữ liệu mô phỏng ngày 08/10/2026. Database được mở chỉ đọc.

## Tải đúng nhánh

Cài Python 3.10 trở lên và Git. Mở PowerShell hoặc terminal rồi chạy:

```powershell
git clone --branch codex/numpy-warehouse-practice --single-branch https://github.com/croznnt/python-sql-dashboard-resources.git
cd python-sql-dashboard-resources/tutorials/numpy-warehouse
```

Nếu đã có repo, chuyển sang nhánh `codex/numpy-warehouse-practice`, sau đó mở terminal trong `tutorials/numpy-warehouse`.

## Chạy trên Windows

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python luong_numpy.py
```

`-m venv` tạo môi trường ảo. `-r` yêu cầu pip đọc danh sách thư viện từ tệp. Lệnh cuối dùng trực tiếp Python trong môi trường vừa tạo, không cần kích hoạt môi trường bằng một lệnh riêng.

## Chạy trên macOS hoặc Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python luong_numpy.py
```

## Chọn database và nơi lưu

```powershell
.venv\Scripts\python luong_numpy.py --db "C:\du_lieu\Warehouse_Automation.db" --out "ket_qua_moi"
```

`--db` chỉ đường dẫn tệp đầu vào. Nếu không truyền, chương trình tìm database cạnh tệp Python. `--out` chọn thư mục báo cáo. Nếu không truyền, báo cáo nằm trong `ket_qua_numpy` cạnh mã nguồn. Chạy lại ghi đè CSV cùng tên.

## Đọc kết quả

| CSV | Nội dung |
| :--- | :--- |
| thiet_bi_numpy.csv | Mã, trạng thái, giờ gốc và số cảnh báo |
| kich_ban_gio.csv | Giờ của bốn thiết bị trong ba kịch bản |
| xep_hang.csv | Thứ tự theo trọng số 0,6 cho giờ và 0,4 cho cảnh báo |
| so_sanh_trong_so.csv | Điểm của hai bộ trọng số trên cùng dữ liệu |

Mở CSV mới và CSV mẫu để so sánh mã, số dòng, tiêu đề cột và giá trị. Chương trình có assert để đối chiếu số liệu mốc và kiểm tra SHA-256 của database trước, sau khi chạy. Thông báo hoàn tất chỉ xuất hiện khi các kiểm tra đều qua.

## Các điểm cần hiểu

1. Mã và giá trị phải có cùng thứ tự. Khi sắp điểm, dùng cùng mảng vị trí để chọn lại mã thiết bị.
2. Kịch bản thêm giờ và xếp hạng là hai nhánh phân tích. Điểm ưu tiên dùng giờ gốc.
3. Trọng số đi theo thứ tự cột đặc trưng: giờ trước, số cảnh báo sau.
4. Mốc giờ, nhãn phân nhóm và trọng số là giả định luyện tập. Điểm không biểu diễn xác suất hỏng hay chính sách bảo trì đã kiểm định.
5. Số cảnh báo là số bản ghi hiện có, chưa phải số sự cố độc lập. Không thấy bản ghi không chứng minh thiết bị chưa từng gặp sự cố.

## Xử lý lỗi thường gặp

| Hiện tượng | Cách kiểm tra |
| :--- | :--- |
| ModuleNotFoundError: numpy | Cài bằng đúng Python trong .venv và dùng Python đó để chạy |
| FileNotFoundError | Kiểm tra đường dẫn --db hoặc đặt database cạnh luong_numpy.py |
| Không thấy báo cáo | Kiểm tra thư mục --out; mặc định là ket_qua_numpy cạnh mã nguồn |
| AssertionError sau khi sửa bài | Tính lại kỳ vọng của kịch bản mới, đối chiếu trước khi cập nhật assert |
| Database khác không qua kiểm tra | Các số mốc chỉ dành cho database mẫu, cần xây kỳ vọng phù hợp dữ liệu mới |

## Nguồn nội dung

Nội dung được phát triển từ các kỹ thuật NumPy và SQL trong Numpy.pdf do người dùng cung cấp, gồm tạo mảng, lọc, đếm nhóm, broadcasting, chuẩn hóa và kiểm chứng. Phần thực hành sử dụng database mô phỏng đi kèm.
