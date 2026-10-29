# Bài 2. Ghép bảng, tổng hợp khu vực và phân công tác vụ

[Về hướng dẫn chung](../README.md)

## Mục tiêu

Hiểu quan hệ khóa khi merge, thay đổi mức chi tiết khi groupby và cách giữ thiết bị chưa có bản ghi ở bảng con. Một báo cáo theo khu vực có ý nghĩa dòng khác với báo cáo theo thiết bị.

## Dữ liệu và yêu cầu

Đọc ThietBi, KhuVuc và TacVuVanHanh thành ba DataFrame.

1. Ghép tên khu vực vào thiết bị theo MaKV.
2. Kiểm tra mỗi thiết bị có khu vực hợp lệ.
3. Thống kê số thiết bị, tổng và trung bình giờ theo khu vực.
4. Đếm tác vụ theo MaTB rồi ghép trở lại bảng thiết bị.
5. Giữ thiết bị chưa có tác vụ, điền số đếm 0 và lưu hai báo cáo.

## Chạy riêng bài 2

```powershell
.venv\Scripts\python luong_pandas.py --bai 2
```

Các đoạn mã dưới đây thuộc hàm bai_2. Biến devices, areas và tasks được đọc từ database trước khi ghép.

## 1. Ghép nhiều thiết bị vào một khu vực

MaKV là cột liên hệ. Mỗi khu vực có thể có nhiều thiết bị, còn bảng khu vực phải có một dòng cho mỗi mã để phép ghép không nhân bản thiết bị.

[Xem code mẫu, dòng 57 đến 63](../luong_pandas.py#L57-L63)

```python
    located = devices.merge(
        areas, on="MaKV", how="left",
        validate="many_to_one", indicator=True
    )
    if not located["_merge"].eq("both").all():
        raise ValueError("Thiết bị thiếu khu vực hợp lệ")
    located = located.drop(columns="_merge")
```


| Tham số | Giá trị | Ý nghĩa |
| :--- | :--- | :--- |
| on | MaKV | Cột dùng làm khóa ghép |
| how | left | Giữ mọi dòng thiết bị ở bảng trái |
| validate | many_to_one | Kiểm tra khóa khu vực ở bảng phải duy nhất |
| indicator | True | Tạo cột _merge để nhận diện nguồn của dòng |

`_merge="both"` nghĩa là dòng đã khớp cả hai phía. left_only báo dòng trái không tìm thấy khu vực. Chương trình báo lỗi khi gặp trường hợp này trước khi bỏ _merge. Chỉ nhìn thấy đủ bốn dòng chưa chứng minh các khóa đã khớp đúng.

## 2. Một dòng cho mỗi khu vực

GROUP BY trong SQL và groupby trong pandas đều gom các dòng theo khóa. Trong bài, khóa gồm cả mã và tên khu vực. as_index=False giữ khóa nhóm thành cột kết quả, thuận tiện khi xuất CSV.

[Xem code mẫu, dòng 64 đến 70](../luong_pandas.py#L64-L70)

```python
    by_area = located.groupby(
        ["MaKV", "TenKV"], as_index=False
    ).agg(
        SoThietBi=("MaTB", "size"),
        TongGio=("GioHoatDong", "sum"),
        GioTrungBinh=("GioHoatDong", "mean")
    ).sort_values("MaKV")
```


Trong agg, mỗi cặp `(cột nguồn, phép tính)` quy định một cột mới. size đếm số dòng thiết bị, sum cộng giờ và mean tính trung bình. count chỉ đếm giá trị không thiếu của cột được chọn; cần phân biệt với size khi dữ liệu có NULL.

| Khu vực | Số thiết bị | Tổng giờ | Trung bình |
| :--- | :--- | :--- | :--- |
| KV01 | 2 | 2060 | 1030 |
| KV02 | 1 | 1500 | 1500 |
| KV03 | 1 | 420 | 420 |

Cộng số thiết bị các nhóm bằng 4; tổng giờ bằng 3980. Nhờ đó có thể đối chiếu với bảng trước khi tổng hợp.

## 3. Đếm tác vụ trước khi ghép

Nếu ghép trực tiếp bảng tác vụ nhiều dòng vào thiết bị rồi cộng giờ, giờ của thiết bị có nhiều tác vụ có thể bị lặp. Tổng hợp bảng con về một dòng trên mỗi MaTB trước khi ghép giữ đúng mức chi tiết.

[Xem code mẫu, dòng 73 đến 80](../luong_pandas.py#L73-L80)

```python
    task_count = tasks.groupby("MaTB", as_index=False).agg(
        SoTacVu=("MaTV", "size")
    )
    assigned = devices[["MaTB", "TenTB", "TrangThai"]].merge(
        task_count, on="MaTB", how="left", validate="one_to_one"
    )
    assigned["SoTacVu"] = assigned["SoTacVu"].fillna(0).astype("Int64")
    assigned = assigned.sort_values("MaTB")
```


`validate="one_to_one"` yêu cầu MaTB duy nhất ở cả hai bảng sau tổng hợp. LEFT JOIN giữ PLC01 dù chưa có tác vụ. Chỉ điền 0 cho cột SoTacVu, vì thiếu số đếm sau phép ghép này có nghĩa không tìm thấy tác vụ tương ứng. Không tự áp dụng fillna(0) cho mọi cột.

astype("Int64") là kiểu số nguyên nullable của pandas, khác với định danh kiểu int64 chữ thường. Bài dùng nó để biểu diễn số đếm dạng nguyên.

| MaTB | SoTacVu |
| :--- | :--- |
| AGV01 | 1 |
| ASRS01 | 1 |
| BC01 | 1 |
| PLC01 | 0 |

## Kết quả và diễn giải

`bai02_khu_vuc.csv` có ba dòng. `bai02_phan_cong.csv` có bốn dòng. Tổng SoTacVu là 3, bằng số dòng TacVuVanHanh. Đây là số tác vụ hiện có trong bảng, chưa phải số tác vụ đang chạy vì bài không lọc trạng thái tác vụ.

## Tự vận dụng

1. Lọc riêng tác vụ có trạng thái DangThucHien trước khi đếm, rồi so sánh với số đếm tất cả tác vụ.
2. Thử tạo bản sao areas và lặp một dòng trong bộ nhớ. Quan sát lỗi validate, không sửa database.
3. Giải thích vì sao inner join với bảng đếm tác vụ có thể làm mất PLC01.

Khi thay định nghĩa số tác vụ, cập nhật tên cột, diễn giải và các assert có liên quan.
