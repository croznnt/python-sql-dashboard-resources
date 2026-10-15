# 🎓 Bài tập 05. Kiểm thử và bàn giao sản phẩm

[Bài trước](04-visualization-sqlalchemy.md) · [Danh sách](README.md)

## 🎯 Đề bài

Hoàn thiện dashboard để một sinh viên khác có thể clone, cài và chạy mà không cần người viết hỗ trợ trực tiếp. Ghi lại kết quả kiểm thử và các giới hạn còn lại để tự đối chiếu.

Đọc trước [tutorial 05](../05-testing-deployment.md). Thời gian dự kiến: 90 đến 120 phút.

## 📋 Yêu cầu bắt buộc

1. Viết ít nhất năm kiểm thử tự động cho module dữ liệu: nạp lại không nhân đôi, tổng toàn bộ, lọc Bắc từ tháng 2 đến tháng 4, dữ liệu rỗng và tổng các khu vực bằng tổng toàn bộ. Dùng database tạm riêng cho kiểm thử, không dùng file database cá nhân.
2. Xác định và kiểm tra hành vi khi tháng bắt đầu sau tháng kết thúc. Có thể bổ sung thành kiểm thử thứ sáu hoặc ghi thành kịch bản tự kiểm tra giao diện.
3. Chạy đầy đủ các kịch bản bài 03, kiểm tra cả biểu đồ đường và biểu đồ cột sau nâng cấp SQLAlchemy.
4. Viết hướng dẫn từ môi trường mới: phiên bản Python, cài phụ thuộc, tạo dữ liệu, cấu hình, chạy dashboard và chạy kiểm thử. Ghi thư mục cần đứng khi chạy từng lệnh.
5. Nhờ một bạn khác làm theo hướng dẫn; ghi lỗi gặp phải và cách sửa. Nếu không có người cùng kiểm tra, tái tạo trong môi trường ảo mới và nêu rõ phương pháp này trong báo cáo.
6. Viết `REPORT.md` gồm mục tiêu, kiến trúc, kết quả kiểm tra, giới hạn và một cải tiến ưu tiên tiếp theo. Phân biệt lỗi cú pháp, lỗi truy vấn và sai kết quả nghiệp vụ.

## ✅ Kết quả tự kiểm tra

Tất cả kiểm thử tự động đều qua; quá trình dựng lại dữ liệu vẫn cho 18 dòng và tổng 15435. Không có đường dẫn chỉ dùng được trên một máy. Không nạp lặp dữ liệu khi đổi widget. Không chứa thông tin xác thực trong mã và lịch sử commit bài thực hành.

Ảnh hoặc video trình diễn phải thể hiện: trạng thái toàn bộ dữ liệu, một bộ lọc có kết quả, một bộ lọc rỗng và tải CSV. Báo cáo ghi phiên bản Python, thư viện cùng kết quả kiểm tra thực tế; không ghi là đã kiểm thử nếu chưa chạy.

## 🌐 Triển khai tùy chọn

Triển khai demo lên môi trường phù hợp theo tutorial 05. Nêu cách tái tạo database trên hosting và cách giữ thông tin kết nối ngoài mã nguồn. Bản chạy cục bộ đầy đủ vẫn đạt yêu cầu bắt buộc, không cần trả phí hoặc đăng ký dịch vụ.

## 💡 Gợi ý

Có thể dùng `unittest` có sẵn trong Python hoặc pytest nếu khai báo phụ thuộc. Tập trung kiểm tra số dòng, tổng doanh thu và điều kiện lọc. Không chỉ kiểm tra hàm có được gọi hoặc app có khởi động.

## 📁 Tệp thực hành

Toàn bộ mã bài 01 đến bài 04 đã hoàn thiện, thư mục `tests/`, hướng dẫn chạy, `REPORT.md` và bằng chứng tự kiểm tra. Bài thực hành cần một lệnh chạy bộ kiểm thử, được ghi rõ trong hướng dẫn.
