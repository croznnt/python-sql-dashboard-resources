# Bài 2. Broadcasting và phân tích kịch bản

[Về hướng dẫn chung](../README.md)

## Mục tiêu

Chuyển một mảng giờ thành ma trận nhiều kịch bản, hiểu chiều tổng hợp và thứ tự điều kiện trong np.select.

## Yêu cầu thực hiện

1. Tạo mảng số giờ giả định thêm: 0, 80, 160.
2. Dùng gio[:, None] để cộng mỗi giờ gốc với cả ba kịch bản.
3. Tính trung bình và số thiết bị đạt 1000 giờ theo từng cột.
4. Phân nhóm Cao khi ít nhất 1200 giờ, Vua khi còn lại ít nhất 800, Thap cho các giá trị khác.

## Hướng dẫn và giải thích

### Broadcasting tạo ma trận nhiều kịch bản

them chứa ba mức thêm giờ giả định: 0, 80 và 160. gio[:, None] thêm một chiều, đổi dạng từ (4,) thành (4,1). Khi cộng với mảng (3,), broadcasting tạo ma trận (4,3).

Mỗi dòng vẫn là một thiết bị. Mỗi cột là một kịch bản. Thao tác tạo mảng mới và không sửa giờ gốc hoặc tệp database.

[Xem trong code mẫu, dòng 59 đến 60](../luong_numpy.py#L59-L60)

```python
    them = np.array([0, 80, 160], dtype=float)
    kich_ban = gio[:, None] + them
```

Số giờ thêm bằng nhau cho mọi thiết bị là giả định mô phỏng. Những cột này không phải lịch sử vận hành thực tế đã được ghi nhận.

### Ý nghĩa axis và phân nhóm có thứ tự

mean(axis=0) tổng hợp qua các dòng để trả một trung bình cho mỗi cột kịch bản. count_nonzero(..., axis=0) đếm số thiết bị đạt 1000 giờ trong từng cột.

np.select chọn nhãn của điều kiện đúng đầu tiên. Phải đặt điều kiện >=1200 trước >=800 vì một giá trị lớn có thể thỏa cả hai. default dùng khi mọi điều kiện đều sai.

[Xem trong code mẫu, dòng 61 đến 66](../luong_numpy.py#L61-L66)

```python
    trung_binh = kich_ban.mean(axis=0)
    vuot_moc = np.count_nonzero(kich_ban >= 1000, axis=0)
    nhom = np.select(
        [kich_ban >= 1200, kich_ban >= 800],
        ["Cao", "Vua"], default="Thap"
    )
```

Ở kịch bản +160, BC01 đạt 1020 giờ nên số thiết bị đạt mốc tăng lên 3. Nhãn Cao, Vua, Thap chỉ biểu diễn các khoảng giờ giả định.

## Kết quả để đối chiếu

Ma trận có dạng (4,3). Trung bình các cột là 995, 1075, 1155. Số thiết bị đạt 1000 giờ là 2, 2, 3. BC01 đạt 1020 giờ ở kịch bản thêm 160 giờ.

## Cách thực hiện tại máy

Đọc đoạn mã tương ứng và dự đoán kết quả trước. Chạy tệp đầy đủ từ thư mục `tutorials/numpy-warehouse` để các biến được tạo theo đúng thứ tự. Các mảnh code trong hướng dẫn cần các biến từ bước trước, không phải script độc lập.

```powershell
.venv\Scripts\python luong_numpy.py
```

Kết quả mới lưu trong `ket_qua_numpy`. Đối chiếu với [CSV mẫu](../ket_qua_mau/).

## Tự vận dụng

Thêm kịch bản +240 giờ, dự đoán shape mới và số thiết bị đạt 1000 giờ. Đổi thứ tự hai điều kiện của np.select, tìm một giá trị bị gắn sai nhãn và giải thích. Khi đổi kịch bản, cập nhật có chủ đích các assert liên quan.
