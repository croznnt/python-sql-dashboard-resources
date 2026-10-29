# Bài 1. Đọc SQL, tạo mảng và lọc thiết bị

[Về hướng dẫn chung](../README.md)

## Mục tiêu

Đọc đúng dữ liệu thiết bị từ SQLite, tạo các mảng cùng thứ tự và lọc bằng điều kiện Boolean.

## Yêu cầu thực hiện

1. Mở database chỉ đọc, lấy MaTB, TrangThai và GioHoatDong theo MaTB.
2. Đếm bản ghi cảnh báo theo thiết bị và căn số đếm theo mảng mã.
3. Kiểm tra shape, dtype và số phần tử. Lọc giờ trong khoảng từ 800 đến 1300, gồm hai biên.
4. Đếm số thiết bị theo trạng thái bằng np.unique và tính tổng giờ.

## Hướng dẫn và giải thích

### Kết nối chỉ đọc và lấy giờ thiết bị

Path.resolve xác định đường dẫn tuyệt đối. Kiểm tra is_file trước khi mở giúp phát hiện sai vị trí ngay từ đầu. Tham số mode=ro trong URI yêu cầu SQLite chỉ đọc tệp, còn uri=True giúp hàm connect hiểu cú pháp này.

SELECT chọn rõ ba cột. ORDER BY MaTB tạo thứ tự ổn định để các mảng mã, trạng thái và giờ giữ quan hệ tương ứng. fetchall trả danh sách các tuple.

[Xem trong code mẫu, dòng 19 đến 29](../luong_numpy.py#L19-L29)

```python
    db = Path(db).resolve()
    if not db.is_file():
        raise FileNotFoundError(db)
    truoc = hashlib.sha256(db.read_bytes()).hexdigest()
    con = sqlite3.connect(db.as_uri() + "?mode=ro", uri=True)
```

```python
        rows = con.execute("""
            SELECT MaTB, TrangThai, GioHoatDong
            FROM ThietBi ORDER BY MaTB
        """).fetchall()
```

Chương trình đóng con trong finally sau khi đọc cả thiết bị và cảnh báo. Phân tích NumPy vẫn tiếp tục được vì dữ liệu đã nằm trong các danh sách Python.

### Đếm cảnh báo và căn theo mã thiết bị

Một cảnh báo tham chiếu MaDL, mẫu đo xác định MaCB và cảm biến xác định MaTB. Chuỗi JOIN này tìm thiết bị của từng cảnh báo. GROUP BY gom về một dòng cho mỗi thiết bị có bản ghi cảnh báo.

dict tạo bảng tra cứu theo mã. get(m, 0) bổ sung số 0 cho thiết bị không có bản ghi cảnh báo trong bảng hiện tại, nhờ đó dem luôn cùng thứ tự với ma.

[Xem trong code mẫu, dòng 30 đến 47](../luong_numpy.py#L30-L47)

```python
        alarm_rows = con.execute("""
            SELECT c.MaTB, COUNT(*)
            FROM CanhBao b
            JOIN DuLieuCamBien d ON d.MaDL=b.MaDL
            JOIN CamBien c ON c.MaCB=d.MaCB
            GROUP BY c.MaTB
        """).fetchall()
```

```python
    bang_dem = dict(alarm_rows)
    dem = np.array([bang_dem.get(m, 0) for m in ma], float)
```

Số 0 ở đây có nghĩa không tìm thấy bản ghi cảnh báo trong tệp. Nó chưa chứng minh thiết bị chưa từng có sự cố trong lịch sử.

### Mảng một chiều và dữ liệu cùng vị trí

np.array tạo mảng từ các cột của kết quả SQL. dtype=str giữ mã và trạng thái dạng chuỗi. dtype=float cho phép tính toán giờ bằng số thực.

shape=(4,) mô tả một mảng một chiều có bốn phần tử, không phải ma trận bốn dòng một cột. Kiểm tra size và isfinite giúp dừng sớm nếu đầu vào rỗng hoặc có số không hữu hạn.

[Xem trong code mẫu, dòng 41 đến 49](../luong_numpy.py#L41-L49)

```python
    ma = np.array([r[0] for r in rows], dtype=str)
    trang_thai = np.array([r[1] for r in rows], dtype=str)
    gio = np.array([r[2] for r in rows], dtype=float)
    if gio.size == 0 or not np.isfinite(gio).all():
        raise ValueError("Cần giờ hoạt động hữu hạn, không rỗng")
```

```python
    print("shape, ndim, size:", gio.shape, gio.ndim, gio.size)
```

Khi dùng cùng lát cắt [1:3] cho ma và gio, kết quả là ASRS01, BC01 và 1500, 860. Vị trí kết thúc 3 không được lấy.

### Lọc Boolean và đếm nhóm bằng NumPy

Hai điều kiện được đặt trong ngoặc và nối bằng &: một thiết bị chỉ được chọn khi giờ vừa không nhỏ hơn 800 vừa không lớn hơn 1300. mask chứa đúng một giá trị True hoặc False cho mỗi thiết bị.

np.unique với return_counts=True trả hai mảng tương ứng: nhãn trạng thái và số lần xuất hiện. zip ghép từng nhãn với số đếm của chính nhãn đó.

[Xem trong code mẫu, dòng 52 đến 56](../luong_numpy.py#L52-L56)

```python
    mask = (gio >= 800) & (gio <= 1300)
    nhan, so_luong = np.unique(trang_thai, return_counts=True)
    print("Từ 800 đến 1300 giờ:", ma[mask], gio[mask].sum())
    print("Trạng thái:", list(zip(nhan, so_luong)))
    print("Tổng, trung bình:", gio.sum(), gio.mean())
```

Hai thiết bị trong khoảng là BC01 và PLC01, tổng 2060 giờ. Các mốc 800 và 1300 là điều kiện của bài, không phải tiêu chuẩn bảo trì.

## Kết quả để đối chiếu

Mã thiết bị: AGV01, ASRS01, BC01, PLC01. Giờ tương ứng: 420, 1500, 860, 1200. Số cảnh báo: 1, 0, 1, 0. Hai thiết bị được lọc là BC01 và PLC01, tổng 2060 giờ. Tổng cả bảng là 3980 giờ.

## Cách thực hiện tại máy

Đọc đoạn mã tương ứng và dự đoán kết quả trước. Chạy tệp đầy đủ từ thư mục `tutorials/numpy-warehouse` để các biến được tạo theo đúng thứ tự. Các mảnh code trong hướng dẫn cần các biến từ bước trước, không phải script độc lập.

```powershell
.venv\Scripts\python luong_numpy.py
```

Kết quả mới lưu trong `ket_qua_numpy`. Đối chiếu với [CSV mẫu](../ket_qua_mau/).

## Tự vận dụng

Đổi khoảng lọc thành từ 900 đến 1500 giờ. In mã và giờ cùng một mặt nạ. Đối chiếu tổng giờ bằng SUM trong SQL. Các mốc giờ này là điều kiện luyện tập.
