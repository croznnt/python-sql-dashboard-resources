# Bài 3. Chuẩn hóa, trọng số và xuất báo cáo

[Về hướng dẫn chung](../README.md)

## Mục tiêu

Kết hợp giờ hoạt động và số cảnh báo thành điểm minh họa, so sánh thứ tự khi đổi trọng số và kiểm tra báo cáo.

## Yêu cầu thực hiện

1. Ghép hai cột đặc trưng giờ gốc và số cảnh báo bằng column_stack.
2. Chuẩn hóa riêng từng cột, xử lý trường hợp cột có độ rộng bằng 0.
3. Dùng @ để tính điểm với trọng số 0,6 và 0,4. Xếp giảm dần bằng argsort.
4. Đổi trọng số thành 0,3 và 0,7, giải thích sự thay đổi.
5. Lưu bốn CSV và chạy các assert cùng phép đối chiếu hash database.

## Hướng dẫn và giải thích

### Chuẩn hóa hai đặc trưng khác thang đo

column_stack tạo hai cột: giờ hoạt động và số bản ghi cảnh báo. Nếu cộng trực tiếp, hàng nghìn giờ sẽ lấn át số đếm 0 hoặc 1. Chuẩn hóa từng cột đưa chúng về khoảng so sánh chung.

Công thức là (x − min) / (max − min). axis=0 tính riêng cho từng cột. Nếu một cột không biến thiên, np.where thay mẫu số 0 bằng 1 để tránh chia cho 0.

[Xem trong code mẫu, dòng 72 đến 76](../luong_numpy.py#L72-L76)

```python
    dac_trung = np.column_stack((gio, dem))
    min_cot = dac_trung.min(axis=0)
    do_rong = np.ptp(dac_trung, axis=0)
    mau_so = np.where(do_rong == 0, 1, do_rong)
    chuan = (dac_trung - min_cot) / mau_so
```

BC01: (860 − 420) / (1500 − 420) = 0,4074. Cột không biến thiên trở thành 0, vì mọi giá trị bằng min của cột đó.

### Tích ma trận và thứ tự ưu tiên

chuan có dạng (4,2), trong_so có dạng (2,). Phép @ tính tổng có trọng số trên mỗi dòng và trả bốn điểm. Trọng số 0,6 dành cho giờ, 0,4 dành cho số cảnh báo, theo đúng thứ tự cột.

argsort trả vị trí sắp xếp, không trả mã thiết bị. Đổi dấu điểm để xếp giảm dần. kind="stable" giữ thứ tự ban đầu khi hai điểm bằng nhau.

[Xem trong code mẫu, dòng 81 đến 83](../luong_numpy.py#L81-L83)

```python
    trong_so = np.array([0.6, 0.4])
    diem = chuan @ trong_so
    thu_tu = np.argsort(-diem, kind="stable")
```

Điểm BC01 = 0,6 × 0,4074 + 0,4 × 1 = 0,6444. Đây là thước đo minh họa được định nghĩa bởi trọng số, không phải xác suất hỏng.

### Đổi trọng số và đọc sự thay đổi

Để khảo sát độ nhạy, giữ nguyên đặc trưng và cách chuẩn hóa, chỉ đổi trọng số sang 0,3 cho giờ và 0,7 cho cảnh báo. Như vậy, chênh lệch thứ tự xuất phát từ quy tắc ưu tiên.

AGV01 có giờ thấp nhất nhưng có một bản ghi cảnh báo. Khi tăng trọng số cảnh báo, thiết bị này lên hạng 2. Cần trình bày cả quy tắc và dữ liệu khi giải thích lựa chọn.

[Xem trong code mẫu, dòng 84 đến 89](../luong_numpy.py#L84-L89)

```python
    trong_so_moi = np.array([0.3, 0.7])
    diem_moi = chuan @ trong_so_moi
    thu_tu_moi = np.argsort(-diem_moi, kind="stable")
    print("Thứ tự 0.6/0.4:", ma[thu_tu])
    print("Điểm:", np.round(diem[thu_tu], 3))
    print("Thứ tự 0.3/0.7:", ma[thu_tu_moi])
```

Có thể thảo luận thiết bị nào cần xem xét trước theo từng mục đích. Không kết luận một bộ trọng số là chính sách đúng chỉ từ bốn thiết bị mẫu.

### Xuất báo cáo và kiểm tra tệp đã lưu

Thư viện csv ghi dữ liệu sau phân tích mà không cần pandas. newline="" để csv quản lý dấu xuống dòng. encoding="utf-8-sig" hỗ trợ mở tiếng Việt trong Excel.

writerow ghi tiêu đề, writerows ghi nhiều dòng. Hàm luu_csv được gọi cho bảng nguồn, kịch bản, thứ tự ưu tiên và so sánh điểm của hai bộ trọng số.

[Xem trong code mẫu, dòng 10 đến 99](../luong_numpy.py#L10-L99)

```python
def luu_csv(path, header, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
```

```python
    luu_csv(output / "kich_ban_gio.csv",
            ["MaTB", "Them0", "Them80", "Them160"],
            ((m, *a) for m, a in zip(ma, kich_ban)))
```

Chạy lại sẽ ghi đè các CSV cùng tên. Tệp kết quả nằm riêng trong ket_qua_numpy, database nguồn tiếp tục mở chỉ đọc.

### Kiểm chứng từ đầu vào đến kết quả

Các assert đối chiếu giả định với bản database bài học: đủ mã thiết bị, tổng giờ đúng, ma trận đúng dạng và thứ tự ưu tiên đúng. np.isclose và np.allclose phù hợp khi so sánh số thực có thể có sai số biểu diễn.

Mã còn so sánh SHA-256 của tệp trước và sau khi chạy. Hash bằng nhau xác nhận nội dung tệp nguồn không thay đổi trong lần thực hiện này.

[Xem trong code mẫu, dòng 109 đến 119](../luong_numpy.py#L109-L119)

```python
    assert ma.tolist() == ["AGV01", "ASRS01", "BC01", "PLC01"]
    assert np.isclose(gio.sum(), 3980)
    assert dem.tolist() == [1, 0, 1, 0]
    assert kich_ban.shape == (4, 3)
    assert np.allclose(trung_binh, [995, 1075, 1155])
    assert vuot_moc.tolist() == [2, 2, 3]
    assert ma[thu_tu].tolist() == ["BC01", "ASRS01", "PLC01", "AGV01"]
    assert ma[thu_tu_moi].tolist() == ["BC01", "AGV01", "ASRS01", "PLC01"]
    sau = hashlib.sha256(db.read_bytes()).hexdigest()
    assert truoc == sau, "Tệp nguồn đã thay đổi"
    print("Đã kiểm chứng kết quả và giữ nguyên database.")
```

Khi dùng database khác, các con số mốc có thể thay đổi. Cần xây lại kỳ vọng theo dữ liệu mới, không xóa kiểm tra chỉ để chương trình chạy tiếp.

## Kết quả để đối chiếu

Với trọng số 0,6/0,4: BC01, ASRS01, PLC01, AGV01. Điểm làm tròn tương ứng 0,644; 0,600; 0,433; 0,400. Với trọng số 0,3/0,7: BC01, AGV01, ASRS01, PLC01.

## Cách thực hiện tại máy

Đọc đoạn mã tương ứng và dự đoán kết quả trước. Chạy tệp đầy đủ từ thư mục `tutorials/numpy-warehouse` để các biến được tạo theo đúng thứ tự. Các mảnh code trong hướng dẫn cần các biến từ bước trước, không phải script độc lập.

```powershell
.venv\Scripts\python luong_numpy.py
```

Kết quả mới lưu trong `ket_qua_numpy`. Đối chiếu với [CSV mẫu](../ket_qua_mau/).

## Tự vận dụng

Thử trọng số 0,5/0,5 và giải thích thứ tự. Tạo một bản sao mảng số cảnh báo toàn 0 trong bộ nhớ để kiểm tra cột không biến thiên. Giữ nguyên database và lưu kết quả mở rộng ở thư mục khác bằng --out. Cập nhật các assert theo quy tắc mới.
