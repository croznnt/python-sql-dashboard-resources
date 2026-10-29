# Luồng thực hành NumPy với dữ liệu kho

Luồng này tổng hợp có chọn lọc từ Numpy.pdf, không thay thế toàn bộ 36 ví dụ. Bài dùng cùng database mô phỏng nhưng tập trung vào thiết bị, kịch bản thêm giờ và độ nhạy của thứ tự ưu tiên.

## Mục tiêu và quy trình

Đọc SQL bằng sqlite3, tạo mảng có cùng thứ tự MaTB, lọc và đếm bằng NumPy, tạo ma trận broadcasting, chuẩn hóa hai đặc trưng, tính điểm bằng tích ma trận và lưu CSV. Không dùng pandas.

## Tệp đi kèm

1. [Slide bài giảng 15 trang](Luong_ThucHanh_NumPy.pptx).
2. [Mã Python hoàn chỉnh](luong_numpy.py).
3. [Database mô phỏng](Warehouse_Automation.db).
4. [Kết quả CSV mẫu](ket_qua_mau/). Chương trình tạo kết quả mới trong `ket_qua_numpy` để tiện đối chiếu.

## Chạy trên máy cá nhân

Sau khi tải hoặc clone repo, mở terminal trong `tutorials/numpy-warehouse`. Tạo môi trường và chạy lần lượt:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python luong_numpy.py
```

Chọn đường dẫn khác bằng `--db "C:\du_lieu\Warehouse_Automation.db"`; chọn thư mục kết quả bằng `--out "ket_qua_moi"`. Các giá trị mốc trong assert chỉ dành cho database đã cung cấp.

## Đọc slide cùng code

Các số bên trái code là số dòng thực tế của luong_numpy.py. Dòng dài có thể xuống hàng khi trình chiếu nhưng không phát sinh số dòng mới. Dấu … biểu diễn phần lược, không phải mã cần nhập. Nên chạy tệp đầy đủ, không chép từng mảnh rời khỏi slide.

### Slide 1. Luồng thực hành NumPy: kịch bản và ưu tiên kiểm tra

Bài thực hành kết nối các kỹ thuật trong Numpy.pdf thành một quy trình có đầu vào và kết quả cuối cùng. Câu hỏi là: khi số giờ và trọng số thay đổi, danh sách thiết bị cần xem xét thay đổi như thế nào?

Mục tiêu là hiểu mảng có nhãn đi kèm, broadcasting, trục tổng hợp và cách tính điểm từ nhiều đặc trưng. SQL chỉ đọc dữ liệu, NumPy thực hiện phân tích, thư viện csv lưu kết quả.

Các kịch bản và trọng số là giả định để học phép tính. Điểm ưu tiên không thay thế quy trình bảo trì hoặc chứng minh thiết bị đang hỏng.

### Slide 2. 1. Đường đi của dữ liệu trong bài

Hai truy vấn SQL cung cấp hai tập dữ liệu có mức chi tiết khác nhau. Bảng thiết bị có một dòng cho mỗi MaTB. Cảnh báo được đếm theo MaTB trước khi đưa về Python, tránh lặp lại số giờ do ghép nhiều dòng con.

Mã thiết bị đóng vai trò nhãn. Khi sắp xếp điểm, cần áp dụng cùng mảng vị trí cho cả nhãn và giá trị để không gắn sai kết quả.

Kịch bản thêm giờ và xếp hạng là hai nhánh phân tích. Điểm ưu tiên trong bài dùng giờ gốc, không tự lấy giờ từ một kịch bản.

### Slide 3. 2. Chuẩn bị thư mục và chạy chương trình

Giải nén gói thực hành rồi mở toàn bộ thư mục trong VS Code. Đặt database cùng thư mục với luong_numpy.py để chương trình tìm tệp mặc định theo vị trí mã nguồn.

Lệnh thứ nhất tạo môi trường ảo. Lệnh thứ hai cài thư viện NumPy trong môi trường đó. Lệnh cuối chạy toàn bộ luồng, tự đóng kết nối rồi tạo ket_qua_numpy.

Nếu database ở thư mục khác, thêm --db "đường_dẫn_đầy_đủ.db" sau tên script. Có thể chọn nơi lưu báo cáo bằng --out "thư_mục_kết_quả".

### Slide 4. 3. Kết nối chỉ đọc và lấy giờ thiết bị

Path.resolve xác định đường dẫn tuyệt đối. Kiểm tra is_file trước khi mở giúp phát hiện sai vị trí ngay từ đầu. Tham số mode=ro trong URI yêu cầu SQLite chỉ đọc tệp, còn uri=True giúp hàm connect hiểu cú pháp này.

SELECT chọn rõ ba cột. ORDER BY MaTB tạo thứ tự ổn định để các mảng mã, trạng thái và giờ giữ quan hệ tương ứng. fetchall trả danh sách các tuple.

Dòng trong tệp mẫu: 19, 20, 21, 22, 23, 26, 27, 28, 29.

Chương trình đóng con trong finally sau khi đọc cả thiết bị và cảnh báo. Phân tích NumPy vẫn tiếp tục được vì dữ liệu đã nằm trong các danh sách Python.

### Slide 5. 4. Đếm cảnh báo và căn theo mã thiết bị

Một cảnh báo tham chiếu MaDL, mẫu đo xác định MaCB và cảm biến xác định MaTB. Chuỗi JOIN này tìm thiết bị của từng cảnh báo. GROUP BY gom về một dòng cho mỗi thiết bị có bản ghi cảnh báo.

dict tạo bảng tra cứu theo mã. get(m, 0) bổ sung số 0 cho thiết bị không có bản ghi cảnh báo trong bảng hiện tại, nhờ đó dem luôn cùng thứ tự với ma.

Dòng trong tệp mẫu: 30, 31, 32, 33, 34, 35, 36, 46, 47.

Số 0 ở đây có nghĩa không tìm thấy bản ghi cảnh báo trong tệp. Nó chưa chứng minh thiết bị chưa từng có sự cố trong lịch sử.

### Slide 6. 5. Mảng một chiều và dữ liệu cùng vị trí

np.array tạo mảng từ các cột của kết quả SQL. dtype=str giữ mã và trạng thái dạng chuỗi. dtype=float cho phép tính toán giờ bằng số thực.

shape=(4,) mô tả một mảng một chiều có bốn phần tử, không phải ma trận bốn dòng một cột. Kiểm tra size và isfinite giúp dừng sớm nếu đầu vào rỗng hoặc có số không hữu hạn.

Dòng trong tệp mẫu: 41, 42, 43, 44, 45, 49.

Khi dùng cùng lát cắt [1:3] cho ma và gio, kết quả là ASRS01, BC01 và 1500, 860. Vị trí kết thúc 3 không được lấy.

### Slide 7. 6. Lọc Boolean và đếm nhóm bằng NumPy

Hai điều kiện được đặt trong ngoặc và nối bằng &: một thiết bị chỉ được chọn khi giờ vừa không nhỏ hơn 800 vừa không lớn hơn 1300. mask chứa đúng một giá trị True hoặc False cho mỗi thiết bị.

np.unique với return_counts=True trả hai mảng tương ứng: nhãn trạng thái và số lần xuất hiện. zip ghép từng nhãn với số đếm của chính nhãn đó.

Dòng trong tệp mẫu: 52, 53, 54, 55, 56.

Hai thiết bị trong khoảng là BC01 và PLC01, tổng 2060 giờ. Các mốc 800 và 1300 là điều kiện của bài, không phải tiêu chuẩn bảo trì.

### Slide 8. 7. Broadcasting tạo ma trận nhiều kịch bản

them chứa ba mức thêm giờ giả định: 0, 80 và 160. gio[:, None] thêm một chiều, đổi dạng từ (4,) thành (4,1). Khi cộng với mảng (3,), broadcasting tạo ma trận (4,3).

Mỗi dòng vẫn là một thiết bị. Mỗi cột là một kịch bản. Thao tác tạo mảng mới và không sửa giờ gốc hoặc tệp database.

Dòng trong tệp mẫu: 59, 60.

Số giờ thêm bằng nhau cho mọi thiết bị là giả định mô phỏng. Những cột này không phải lịch sử vận hành thực tế đã được ghi nhận.

### Slide 9. 8. Ý nghĩa axis và phân nhóm có thứ tự

mean(axis=0) tổng hợp qua các dòng để trả một trung bình cho mỗi cột kịch bản. count_nonzero(..., axis=0) đếm số thiết bị đạt 1000 giờ trong từng cột.

np.select chọn nhãn của điều kiện đúng đầu tiên. Phải đặt điều kiện >=1200 trước >=800 vì một giá trị lớn có thể thỏa cả hai. default dùng khi mọi điều kiện đều sai.

Dòng trong tệp mẫu: 61, 62, 63, 64, 65, 66.

Ở kịch bản +160, BC01 đạt 1020 giờ nên số thiết bị đạt mốc tăng lên 3. Nhãn Cao, Vua, Thap chỉ biểu diễn các khoảng giờ giả định.

### Slide 10. 9. Chuẩn hóa hai đặc trưng khác thang đo

column_stack tạo hai cột: giờ hoạt động và số bản ghi cảnh báo. Nếu cộng trực tiếp, hàng nghìn giờ sẽ lấn át số đếm 0 hoặc 1. Chuẩn hóa từng cột đưa chúng về khoảng so sánh chung.

Công thức là (x − min) / (max − min). axis=0 tính riêng cho từng cột. Nếu một cột không biến thiên, np.where thay mẫu số 0 bằng 1 để tránh chia cho 0.

Dòng trong tệp mẫu: 72, 73, 74, 75, 76.

BC01: (860 − 420) / (1500 − 420) = 0,4074. Cột không biến thiên trở thành 0, vì mọi giá trị bằng min của cột đó.

### Slide 11. 10. Tích ma trận và thứ tự ưu tiên

chuan có dạng (4,2), trong_so có dạng (2,). Phép @ tính tổng có trọng số trên mỗi dòng và trả bốn điểm. Trọng số 0,6 dành cho giờ, 0,4 dành cho số cảnh báo, theo đúng thứ tự cột.

argsort trả vị trí sắp xếp, không trả mã thiết bị. Đổi dấu điểm để xếp giảm dần. kind="stable" giữ thứ tự ban đầu khi hai điểm bằng nhau.

Dòng trong tệp mẫu: 81, 82, 83.

Điểm BC01 = 0,6 × 0,4074 + 0,4 × 1 = 0,6444. Đây là thước đo minh họa được định nghĩa bởi trọng số, không phải xác suất hỏng.

### Slide 12. 11. Đổi trọng số và đọc sự thay đổi

Để khảo sát độ nhạy, giữ nguyên đặc trưng và cách chuẩn hóa, chỉ đổi trọng số sang 0,3 cho giờ và 0,7 cho cảnh báo. Như vậy, chênh lệch thứ tự xuất phát từ quy tắc ưu tiên.

AGV01 có giờ thấp nhất nhưng có một bản ghi cảnh báo. Khi tăng trọng số cảnh báo, thiết bị này lên hạng 2. Cần trình bày cả quy tắc và dữ liệu khi giải thích lựa chọn.

Dòng trong tệp mẫu: 84, 85, 86, 87, 88, 89.

Có thể thảo luận thiết bị nào cần xem xét trước theo từng mục đích. Không kết luận một bộ trọng số là chính sách đúng chỉ từ bốn thiết bị mẫu.

### Slide 13. 12. Xuất báo cáo và kiểm tra tệp đã lưu

Thư viện csv ghi dữ liệu sau phân tích mà không cần pandas. newline="" để csv quản lý dấu xuống dòng. encoding="utf-8-sig" hỗ trợ mở tiếng Việt trong Excel.

writerow ghi tiêu đề, writerows ghi nhiều dòng. Hàm luu_csv được gọi cho bảng nguồn, kịch bản, thứ tự ưu tiên và so sánh điểm của hai bộ trọng số.

Dòng trong tệp mẫu: 10, 11, 12, 13, 14, 97, 98, 99.

Chạy lại sẽ ghi đè các CSV cùng tên. Tệp kết quả nằm riêng trong ket_qua_numpy, database nguồn tiếp tục mở chỉ đọc.

### Slide 14. 13. Kiểm chứng từ đầu vào đến kết quả

Các assert đối chiếu giả định với bản database bài học: đủ mã thiết bị, tổng giờ đúng, ma trận đúng dạng và thứ tự ưu tiên đúng. np.isclose và np.allclose phù hợp khi so sánh số thực có thể có sai số biểu diễn.

Mã còn so sánh SHA-256 của tệp trước và sau khi chạy. Hash bằng nhau xác nhận nội dung tệp nguồn không thay đổi trong lần thực hiện này.

Dòng trong tệp mẫu: 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119.

Khi dùng database khác, các con số mốc có thể thay đổi. Cần xây lại kỳ vọng theo dữ liệu mới, không xóa kiểm tra chỉ để chương trình chạy tiếp.

### Slide 15. 14. Bài thực hành tự vận dụng

Dùng lại luong_numpy.py nhưng lưu kết quả mở rộng sang thư mục khác để giữ bộ kết quả đã đối chiếu. Trước mỗi thay đổi, dự đoán hình dạng mảng và kết quả rồi mới chạy chương trình.

Giữ nguyên database. Trình bày câu SQL, đoạn NumPy đã sửa, bảng kết quả và giải thích kết luận. Các yêu cầu dưới đây tiếp tục sử dụng cùng dữ liệu thiết bị.

Khi thay kịch bản hoặc trọng số, phải cập nhật các assert liên quan theo kết quả tự tính. Cột cảnh báo toàn 0 là dữ liệu giả định trong mảng, không sửa bảng nguồn.

## Nguồn và giả định

Nguồn: Numpy.pdf, các ví dụ 01 đến 06, 09, 10, 12, 26 đến 28, 36 và bài D. Database do người dùng cung cấp.

Kịch bản thêm 0, 80, 160 giờ; mốc 800, 1000, 1200 giờ; trọng số 0,6/0,4 và 0,3/0,7 đều là quy tắc luyện tập. Số cảnh báo đếm các bản ghi hiện có, không phải số sự cố độc lập. Điểm không biểu diễn xác suất hỏng.

SQL chỉ đọc tệp. CSV nằm trong thư mục riêng và được ghi đè khi chạy lại. Các bước lưu dùng thư viện csv của Python.
