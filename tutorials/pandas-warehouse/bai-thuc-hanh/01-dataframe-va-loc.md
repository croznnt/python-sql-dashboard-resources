# Bài 1. Đọc SQL, khám phá DataFrame và lọc thiết bị

[Về hướng dẫn chung](../README.md)

## Mục tiêu

Đọc kết quả SQL thành bảng có nhãn, kiểm tra kích thước và kiểu dữ liệu, chọn dòng theo trạng thái rồi tính thống kê mô tả. Cần giải thích được mỗi dòng kết quả đại diện cho thiết bị nào.

## Dữ liệu và yêu cầu

Dùng bảng ThietBi gồm bốn thiết bị. Các cột quan trọng là MaTB, TrangThai và GioHoatDong.

1. Đọc toàn bảng theo thứ tự MaTB.
2. Kiểm tra shape, dtypes và chuyển giờ sang số.
3. Giữ thiết bị DangChay, chỉ lấy mã, tên và giờ.
4. Tính count, sum, mean, median, min và max cho giờ của cả bảng.
5. Lưu hai CSV và đối chiếu kết quả.

## Chạy riêng bài 1

Chạy từ thư mục `tutorials/pandas-warehouse` sau khi cài môi trường theo README chung.

```powershell
.venv\Scripts\python luong_pandas.py --bai 1
```

Mỗi bài tự đọc dữ liệu cần dùng nên không cần chạy bài khác trước. Các đoạn mã dưới đây nằm trong hàm bai_1, dùng kết nối con và thư mục output do chương trình chính truyền vào.

## 1. DataFrame, Series và kiểm tra kiểu

DataFrame là bảng hai chiều có nhãn dòng, nhãn cột. Một cột chọn bằng `devices["GioHoatDong"]` là Series. Chọn một danh sách cột bằng `devices[["MaTB"]]` vẫn giữ DataFrame.

shape trả cặp số dòng, số cột. dtypes mô tả kiểu từng cột. Chỉ số dòng của DataFrame giúp định vị dữ liệu nhưng không mặc nhiên là khóa nghiệp vụ MaTB.

[Xem code mẫu, dòng 16 đến 25](../luong_pandas.py#L16-L25)

```python
    devices = pd.read_sql_query(
        "SELECT * FROM ThietBi ORDER BY MaTB", con
    )
    devices["GioHoatDong"] = pd.to_numeric(
        devices["GioHoatDong"], errors="raise"
    )
    if devices["GioHoatDong"].isna().any():
        raise ValueError("Thiếu giờ hoạt động")
    print("Kích thước:", devices.shape)
    print("Kiểu cột:\n", devices.dtypes)
```


`pd.read_sql_query(sql, con)` thực thi câu SELECT qua kết nối con và trả DataFrame. ORDER BY bảo đảm thứ tự rõ ràng. `pd.to_numeric(..., errors="raise")` chuyển cột sang số và báo lỗi nếu gặp chuỗi không chuyển được. isna nhận diện dữ liệu thiếu, any kiểm tra có ít nhất một vị trí thiếu hay không.

Kiểu chuỗi có thể hiển thị khác nhau giữa các phiên bản pandas, chẳng hạn str hoặc object. Điều cần kiểm tra ở đây là cột giờ có thể tính số và không có giá trị thiếu.

## 2. Lọc dòng bằng loc

Phép eq tạo Series Boolean theo từng dòng. loc nhận mặt nạ ở phía trước dấu phẩy và danh sách cột ở phía sau. Vì vậy, một câu lệnh vừa chọn thiết bị phù hợp vừa chọn đúng thông tin cần báo cáo.

[Xem code mẫu, dòng 28 đến 31](../luong_pandas.py#L28-L31)

```python
    mask = devices["TrangThai"].eq("DangChay")
    columns = ["MaTB", "TenTB", "GioHoatDong"]
    running = devices.loc[mask, columns].copy()
    running = running.sort_values("MaTB")
```


`copy()` tạo bảng kết quả riêng để các thao tác tiếp theo thể hiện rõ ý định xử lý. `sort_values("MaTB")` sắp dòng theo mã. Mặt nạ được tạo trực tiếp từ devices nên index khớp với bảng được lọc. Không dùng toán tử and hoặc or của Python giữa các Series; dùng & hoặc | và đặt từng điều kiện trong ngoặc.

## 3. Thống kê toàn bảng

agg nhận danh sách phép tổng hợp. Nó tạo một Series, trong đó nhãn là tên phép tính. rename_axis đặt tên nhãn là ChiTieu, reset_index đưa nhãn thành cột và đặt tên cột giá trị là GiaTri.

[Xem code mẫu, dòng 32 đến 34](../luong_pandas.py#L32-L34)

```python
    summary = devices["GioHoatDong"].agg(
        ["count", "sum", "mean", "median", "min", "max"]
    ).rename_axis("ChiTieu").reset_index(name="GiaTri")
```


| Chỉ tiêu | Kết quả | Cách đọc |
| :--- | :--- | :--- |
| count | 4 | Số giờ có dữ liệu |
| sum | 3980 | Tổng giờ tích lũy |
| mean | 995 | Tổng chia bốn thiết bị |
| median | 1030 | Trung bình của hai vị trí giữa sau sắp xếp |
| min / max | 420 / 1500 | Hai cực trị của bốn thiết bị |

Đây là thống kê của toàn bảng devices. Nếu tính trên running, tập được xét chỉ còn hai thiết bị và kết quả sẽ khác. Các giờ là dữ liệu tích lũy, chưa mô tả riêng một ca làm việc.

## Kết quả và tệp đầu ra

`bai01_dang_chay.csv` có BC01 với 860 giờ và PLC01 với 1200 giờ. `bai01_thong_ke_gio.csv` có sáu chỉ tiêu ở bảng trên. Trong CSV thống kê, count có thể ghi 4.0 vì Series kết quả dùng chung kiểu số thực. Điều này vẫn biểu diễn bốn giá trị.

Các CSV nằm trong ket_qua_pandas. index=False khi xuất chỉ bỏ chỉ số dòng khỏi tệp, không xóa cột MaTB.

## Tự vận dụng

1. Lọc thiết bị đang chạy và có ít nhất 1000 giờ, dùng hai điều kiện nối bằng &.
2. Tính trung bình giờ riêng cho running, rồi giải thích vì sao khác 995.
3. Đổi thứ tự theo giờ giảm dần và giữ mã đi cùng giá trị.

Lưu biến thể ở tệp khác để còn đối chiếu CSV mẫu. Mốc 1000 giờ là điều kiện luyện tập.
