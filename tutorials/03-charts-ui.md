# 📈 Bài 03. Biểu đồ và giao diện

[Bài trước](02-sql-pandas.md) · [Lộ trình](README.md) · [Bài tiếp theo](04-external-databases.md)

## 1. Đọc cấu trúc ứng dụng

`st.set_page_config` đặt tiêu đề tab và bố cục. `st.title` và `st.caption` cung cấp ngữ cảnh. `st.selectbox` trả về khu vực đã chọn. Giá trị đó được đưa vào tham số truy vấn, sau đó DataFrame cung cấp dữ liệu cho `st.metric`, biểu đồ và `st.dataframe`.

Streamlit chạy lại script khi thay đổi widget. Trong demo nhỏ, tạo lại dữ liệu giúp mỗi lượt có cùng điểm xuất phát. Với cơ sở dữ liệu thật, cần quản lý engine, độ mới dữ liệu và chi phí truy vấn thay vì nạp lại toàn bộ dữ liệu.

## 2. Vẽ biểu đồ đường

```python
figure, axis = plt.subplots(figsize=(10, 4))
try:
    sns.lineplot(data=data, x="month", y="revenue", hue="region", marker="o", ax=axis)
    axis.set(xlabel="Tháng", ylabel="Doanh thu")
    figure.tight_layout()
    st.pyplot(figure)
finally:
    plt.close(figure)
```

`figure` là toàn bộ hình; `axis` là vùng trục. `hue` chia màu theo khu vực. Truyền `ax` để Seaborn vẽ đúng trục, rồi đưa Figure đó cho Streamlit. Đóng Figure sau khi hiển thị để giải phóng tài nguyên.

Demo chỉ có một quan sát cho mỗi cặp tháng và khu vực. Nếu dữ liệu thật có nhiều dòng cho cùng cặp, cần tổng hợp theo nghiệp vụ trước khi vẽ, vì lineplot mặc định có cơ chế ước lượng thống kê.

## 3. Thêm biểu đồ cột

Sau khi tạo `totals` theo bài 02, chèn đoạn này sau biểu đồ đường. Đặt tên Figure riêng để dễ theo dõi:

```python
st.subheader("Doanh thu theo khu vực")
bar_figure, bar_axis = plt.subplots(figsize=(8, 4))
try:
    sns.barplot(data=totals, x="region", y="total_revenue", ax=bar_axis)
    bar_axis.set(xlabel="Khu vực", ylabel="Tổng doanh thu")
    bar_figure.tight_layout()
    st.pyplot(bar_figure)
finally:
    plt.close(bar_figure)
```

Bạn sẽ thấy Nam cao nhất, rồi Trung và Bắc. Muốn biểu đồ phản ánh bộ lọc, thêm cùng điều kiện WHERE và tham số vào truy vấn tổng hợp trước GROUP BY.

## 4. Bổ sung tải CSV

Chèn sau phần bảng dữ liệu:

```python
st.download_button(
    "Tải dữ liệu đang lọc",
    data=data.to_csv(index=False).encode("utf-8-sig"),
    file_name="sales.csv",
    mime="text/csv",
)
```

File chỉ chứa các dòng đang lọc. Kiểm tra số dòng và tổng doanh thu sau khi mở file.

## 5. Xử lý dữ liệu rỗng

Ngay sau truy vấn, trước metric và biểu đồ, thêm:

```python
if data.empty:
    st.info("Không có dữ liệu phù hợp bộ lọc.")
    st.stop()
```

Với dữ liệu thật, cần xác định cách xử lý giá trị NULL, kiểu ngày tháng, đơn vị doanh thu và múi giờ trước khi chọn biểu đồ.

## 📖 Nguồn

1. [Seaborn lineplot](https://seaborn.pydata.org/generated/seaborn.lineplot.html).
2. [Streamlit pyplot](https://docs.streamlit.io/develop/api-reference/charts/st.pyplot).
3. [Matplotlib pyplot](https://matplotlib.org/stable/api/pyplot_summary.html).

## 🧑‍💻 Thực hành sau bài học

[Làm bài tập 03](exercises/03-dashboard-filters.md), xem yêu cầu, kết quả cần đạt và hướng dẫn thực hành.
