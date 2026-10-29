# Bài 3. Thời gian, dữ liệu thiếu và bảng cảm biến

[Về hướng dẫn chung](../README.md)

## Mục tiêu

Ghép mẫu đo với cấu hình, xử lý cột thời gian và tạo các cách nhìn khác nhau từ cùng dữ liệu. Cần phân biệt thiếu ngưỡng với thiếu phép đo, và hiểu vì sao sắp xếp quyết định mẫu mới nhất.

## Dữ liệu và yêu cầu

Dùng DuLieuCamBien có sáu mẫu và CamBien có bốn cấu hình.

1. Truy vấn mẫu từ ngày 2026-10-08 bằng tham số SQL.
2. Ghép cấu hình theo MaCB và chuyển kiểu thời gian, số.
3. Chọn mẫu thấp hơn cận dưới hoặc cao hơn cận trên đã khai báo.
4. Lấy mẫu mới nhất mỗi cảm biến.
5. Pivot thành bảng thời điểm nhân cảm biến và lưu ba CSV.

## Chạy riêng bài 3

```powershell
.venv\Scripts\python luong_pandas.py --bai 3
```

Đoạn mã trong trang thuộc hàm bai_3. Hàm tự đọc dữ liệu và kiểm tra trước khi xuất báo cáo.

## 1. Truy vấn có tham số

Dấu ? giữ vị trí cho mốc bắt đầu. params truyền giá trị riêng khỏi cấu trúc SQL. Tuple một phần tử cần dấu phẩy cuối. ORDER BY MaDL giữ thứ tự mẫu ổn định.

[Xem code mẫu, dòng 93 đến 96](../luong_pandas.py#L93-L96)

```python
    readings = pd.read_sql_query(
        "SELECT * FROM DuLieuCamBien WHERE ThoiDiem >= ? ORDER BY MaDL",
        con, params=("2026-10-08 00:00:00",)
    )
```


Mốc thời gian dùng định dạng ISO cùng dữ liệu nguồn. Không nối giá trị đầu vào trực tiếp vào chuỗi SQL. Hàm read_sql_query trả DataFrame chứ không tự cập nhật bảng SQLite.

## 2. Ghép và kiểm tra dữ liệu

Mỗi mẫu phải nhận đúng cấu hình của cảm biến tạo ra nó. many_to_one kiểm tra một MaCB ở bảng cấu hình chỉ có một dòng. Sau ghép, cột _merge được kiểm tra rồi mới bỏ.

[Xem code mẫu, dòng 100 đến 110](../luong_pandas.py#L100-L110)

```python
    data = readings.merge(
        sensors, on="MaCB", how="left",
        validate="many_to_one", indicator=True
    )
    if not data["_merge"].eq("both").all():
        raise ValueError("Mẫu đo thiếu cấu hình cảm biến")
    data = data.drop(columns="_merge")
    data["ThoiDiem"] = pd.to_datetime(data["ThoiDiem"], errors="raise")
    data["GiaTri"] = pd.to_numeric(data["GiaTri"], errors="raise")
    if data[["ThoiDiem", "GiaTri"]].isna().any().any():
        raise ValueError("Thiếu thời điểm hoặc giá trị đo")
```


to_datetime chuyển chuỗi thành thời gian để có thể sắp xếp, tính chênh lệch và pivot. to_numeric chuyển giá trị đo thành số. errors="raise" báo lỗi chuyển kiểu, nhưng dữ liệu thiếu vẫn có thể tồn tại nên bài kiểm tra thêm isna. Với DataFrame, any().any() lần lượt rút theo từng cột rồi kiểm tra toàn bảng.

Các thời điểm trong tệp chưa ghi múi giờ. Bài coi chúng thuộc cùng một bối cảnh thời gian, chưa xử lý việc ghép nhiều múi giờ.

## 3. Thiếu cận và mặt nạ vượt ngưỡng

NULL ở cận được đọc thành giá trị thiếu. notna nhận diện vị trí có cận để chỉ so sánh khi giới hạn đó được khai báo. Thiếu ngưỡng dưới không có nghĩa ngưỡng dưới bằng 0.

[Xem code mẫu, dòng 113 đến 117](../luong_pandas.py#L113-L117)

```python
    low = data["NguongDuoi"].notna() & data["GiaTri"].lt(data["NguongDuoi"])
    high = data["NguongTren"].notna() & data["GiaTri"].gt(data["NguongTren"])
    data["VuotNguong"] = (low | high).astype("Int64")
    columns = ["MaDL", "MaCB", "MaTB", "ThoiDiem", "GiaTri", "DonVi"]
    abnormal = data.loc[data["VuotNguong"].eq(1), columns].copy()
```


lt là so sánh nhỏ hơn, gt là lớn hơn. & yêu cầu đồng thời có cận và vi phạm cận; | kết hợp vi phạm dưới hoặc trên. Các dấu < và > nghĩa là bằng đúng cận chưa bị đánh dấu. VuotNguong là nhãn 0 hoặc 1, không phải mức độ hỏng.

| MaDL | Cảm biến | Thiết bị | Giá trị | Đơn vị | Lý do |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 2 | CB01 | BC01 | 68 | degC | Lớn hơn cận trên 55 |
| 5 | CB03 | AGV01 | 18 | % | Nhỏ hơn cận dưới 20 |

## 4. Mẫu mới nhất của mỗi cảm biến

Một dòng ở cuối bảng chưa chắc có thời điểm lớn nhất. Sắp xếp theo ThoiDiem, MaDL trước rồi mới lấy dòng cuối mỗi nhóm MaCB. Nếu hai mẫu cùng thời điểm, MaDL là quy tắc phụ để lựa chọn nhất quán.

[Xem code mẫu, dòng 119 đến 121](../luong_pandas.py#L119-L121)

```python
    latest = data.sort_values(["ThoiDiem", "MaDL"]).groupby(
        "MaCB", sort=False
    ).tail(1).sort_values("MaCB")
```


groupby(..., sort=False) không sắp khóa nhóm. tail(1) giữ một dòng cuối của mỗi nhóm theo thứ tự dữ liệu hiện tại. sort_values("MaCB") cuối cùng chỉ sắp cách trình bày kết quả. Giá trị mới nhất theo CB01, CB02, CB03, CB04 là 68, 1, 18, 2.1.

## 5. Pivot và ý nghĩa ô thiếu

Bảng dài có một dòng cho mỗi mẫu. pivot tạo dạng rộng: mỗi dòng là thời điểm, mỗi cột là cảm biến và ô là giá trị đo. Một cặp (ThoiDiem, MaCB) phải tương ứng tối đa một mẫu.

[Xem code mẫu, dòng 122 đến 126](../luong_pandas.py#L122-L126)

```python
    if data.duplicated(["ThoiDiem", "MaCB"]).any():
        raise ValueError("Cần quy tắc xử lý mẫu trùng trước pivot")
    matrix = data.pivot(
        index="ThoiDiem", columns="MaCB", values="GiaTri"
    ).sort_index().rename_axis(columns=None).reset_index()
```


| Tham số | Vai trò |
| :--- | :--- |
| index="ThoiDiem" | Chọn khóa dòng |
| columns="MaCB" | Chọn nhãn cột |
| values="GiaTri" | Chọn dữ liệu điền vào ô |

sort_index sắp mốc thời gian; rename_axis(columns=None) bỏ tên trục cột để tiêu đề tệp rõ ràng; reset_index đưa thời điểm thành cột trước khi xuất với index=False.

| Thời điểm | CB01 | CB02 | CB03 | CB04 |
| :--- | :--- | :--- | :--- | :--- |
| 08:00 | 42 | Thiếu | 65 | Thiếu |
| 08:05 | 68 | 1 | 18 | 2.1 |

Hai ô thiếu có nghĩa không có phép đo tại mốc đó, không phải số 0. Các cảm biến có đơn vị khác nhau nên không cộng hoặc tính trung bình ngang qua các cột. Khi dữ liệu trùng cặp khóa, bài báo lỗi để yêu cầu quy tắc xử lý thay vì tự chọn một phép tổng hợp.

## Kết quả và tệp đầu ra

1. bai03_vuot_nguong.csv: hai mẫu MaDL 2 và 5, kèm MaTB và đơn vị.
2. bai03_moi_nhat.csv: bốn dòng, mỗi cảm biến một mẫu mới nhất.
3. bai03_ma_tran.csv: hai dòng thời gian, bốn cột cảm biến và cột ThoiDiem. Hai ô thiếu xuất thành ô trống trong CSV.

## Tự vận dụng

1. Dùng dt.hour và dt.minute để tạo cột giờ, phút cho mẫu đo.
2. Chỉ lấy CB01, tính chênh lệch thời điểm và giá trị bằng diff. Giải thích đơn vị của tốc độ thay đổi.
3. Thử thêm một mẫu trùng khóa trong bản sao DataFrame và quan sát lỗi trước pivot. Đề xuất quy tắc chọn hoặc tổng hợp có lý do.

Giữ nguyên database. Dữ liệu ít chỉ hỗ trợ mô tả mẫu đang có, chưa đủ kết luận xu hướng dài hạn.
