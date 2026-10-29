# Thực hành pandas với dữ liệu kho

Bộ thực hành dùng pandas để đưa SQL thành DataFrame, chọn dữ liệu, ghép bảng và tạo báo cáo cảm biến. Ba bài có thể chạy riêng nhưng nên đọc theo thứ tự để nắm được quan hệ giữa nhãn dòng, khóa nghiệp vụ và mức chi tiết của báo cáo.

## Lộ trình

| Bài | Nội dung | Kết quả |
| :--- | :--- | :--- |
| [1. DataFrame và lọc](bai-thuc-hanh/01-dataframe-va-loc.md) | read_sql_query, dtypes, loc, agg | Hai CSV thiết bị và thống kê |
| [2. Merge và groupby](bai-thuc-hanh/02-merge-va-groupby.md) | validate, indicator, groupby, fillna | Hai CSV khu vực và phân công |
| [3. Thời gian và cảm biến](bai-thuc-hanh/03-thoi-gian-va-cam-bien.md) | to_datetime, mặt nạ, tail, pivot | Ba CSV mẫu vượt, mới nhất và ma trận |

Mỗi bài có mục tiêu, yêu cầu, code minh họa, giải thích tham số, kết quả đối chiếu và phần tự vận dụng. Toàn bộ code nằm trong [luong_pandas.py](luong_pandas.py). Các đoạn trong hướng dẫn là phần trích có ngữ cảnh, hãy chạy tệp đầy đủ theo lệnh tương ứng.

## Tệp đi kèm

1. [luong_pandas.py](luong_pandas.py): chương trình ba bài có thể chạy độc lập.
2. [requirements.txt](requirements.txt): pandas và khoảng phiên bản hỗ trợ.
3. [Warehouse_Automation.db](Warehouse_Automation.db): database mô phỏng, cùng bộ dữ liệu của thực hành NumPy.
4. [ket_qua_mau](ket_qua_mau/): bảy CSV dùng để đối chiếu.

Dữ liệu mô phỏng ngày 08/10/2026 gồm bốn thiết bị, ba khu vực, ba tác vụ, bốn cảm biến và sáu mẫu đo. Chương trình mở database chỉ đọc, tự đóng kết nối và kiểm tra hash tệp trước, sau khi chạy.

## Tải nhánh thực hành

Chuẩn bị Python 3.11 trở lên và Git. Chạy trong terminal:

```powershell
git clone --branch codex/pandas-warehouse-practice --single-branch https://github.com/croznnt/python-sql-dashboard-resources.git
cd python-sql-dashboard-resources/tutorials/pandas-warehouse
```

Nếu đã có repo, chuyển sang nhánh codex/pandas-warehouse-practice rồi mở terminal trong tutorials/pandas-warehouse. Có thể tải ZIP của nhánh từ GitHub nếu không dùng Git.

## Cài và chạy trên Windows

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python luong_pandas.py
```

`-m venv` tạo môi trường ảo. `-r` yêu cầu pip cài theo tệp requirements.txt. Dùng trực tiếp Python trong .venv giúp cài và chạy cùng môi trường.

## Cài và chạy trên macOS hoặc Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python luong_pandas.py
```

## Chạy riêng một bài

```powershell
.venv\Scripts\python luong_pandas.py --bai 1
.venv\Scripts\python luong_pandas.py --bai 2
.venv\Scripts\python luong_pandas.py --bai 3
```

`--bai` nhận 1, 2, 3 hoặc all. Mặc định all chạy cả ba. Mỗi hàm tự đọc bảng cần dùng, không phụ thuộc biến tạo bởi bài khác. Trên macOS/Linux, thay đường dẫn Python bằng `.venv/bin/python`.

## Đường dẫn và kết quả

```powershell
.venv\Scripts\python luong_pandas.py --bai 3 --db "C:\du_lieu\Warehouse_Automation.db" --out "ket_qua_moi"
```

`--db` chọn tệp SQLite. Mặc định tìm database cạnh mã nguồn. `--out` chọn nơi lưu CSV, mặc định là ket_qua_pandas cạnh mã nguồn. Chạy lại ghi đè tệp cùng tên. Kết quả tự tạo được Git bỏ qua, còn ket_qua_mau giữ dữ liệu đối chiếu.

| Tệp CSV | Số dòng dữ liệu dự kiến |
| :--- | :--- |
| bai01_dang_chay.csv | 2 |
| bai01_thong_ke_gio.csv | 6 |
| bai02_khu_vuc.csv | 3 |
| bai02_phan_cong.csv | 4 |
| bai03_vuot_nguong.csv | 2 |
| bai03_moi_nhat.csv | 4 |
| bai03_ma_tran.csv | 2 |

## Kiểm chứng và cách đọc

Các assert kiểm tra mã bản ghi, số dòng, tổng giờ và ô thiếu của đúng database mẫu. Thông báo thành công chỉ xuất hiện sau khi các kiểm tra của bài được chọn đều qua. Để đối chiếu, mở CSV mới và CSV mẫu, so tên cột, mã, số dòng và đơn vị. Ô thiếu có thể xuất thành ô trống trong CSV.

Phép ghép phải đúng khóa trước khi tổng hợp. Một dòng theo khu vực khác một dòng theo thiết bị hoặc theo mẫu đo. count bỏ qua dữ liệu thiếu, còn size đếm số dòng. Không thay mọi NULL bằng 0, không tính chung các cột cảm biến khác đơn vị.

## Lỗi thường gặp

| Hiện tượng | Hướng xử lý |
| :--- | :--- |
| Không import được pandas | Cài bằng đúng Python .venv dùng để chạy |
| FileNotFoundError | Kiểm tra --db hoặc đặt database cạnh mã Python |
| MergeError | Kiểm tra tính duy nhất của khóa, không bỏ validate để che lỗi |
| Lỗi chuyển datetime hoặc số | Xem giá trị đầu vào không đúng kiểu, không tự ép bỏ lỗi |
| Lỗi trước pivot | Xác định quy tắc xử lý mẫu trùng cặp thời điểm, cảm biến |
| AssertionError sau khi sửa bài | Tính lại kỳ vọng và cập nhật kiểm tra có chủ đích |

## Giới hạn và tự vận dụng

Các số đối chiếu chỉ dành cho database mô phỏng đi kèm. Khi dùng dữ liệu khác, cần xây kỳ vọng mới. Số tác vụ là số bản ghi hiện có, chưa mặc nhiên là tác vụ đang chạy. Mẫu vượt ngưỡng không chứng minh cảm biến đã hỏng. Bốn cảm biến không có cùng đơn vị nên cần thống kê riêng.

## Tài liệu đọc thêm

1. [pandas read_sql_query](https://pandas.pydata.org/docs/reference/api/pandas.read_sql_query.html).
2. [pandas merge](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html).
3. [pandas groupby](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html).
4. [pandas pivot](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pivot.html).
5. [pandas to_datetime](https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html).
