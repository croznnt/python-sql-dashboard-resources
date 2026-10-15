import sqlite3

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="SQL Dashboard", layout="wide")
st.title("Doanh thu từ SQLite")
st.caption("Dữ liệu giả lập trong bộ nhớ.")
region = st.selectbox("Khu vực", ["Tất cả", "Bắc", "Trung", "Nam"])
connection = sqlite3.connect(":memory:")
try:
    connection.execute("CREATE TABLE sales (month TEXT, region TEXT, revenue REAL)")
    connection.executemany(
        "INSERT INTO sales VALUES (?, ?, ?)",
        [(f"2026-{month:02d}", area, month * 125 + offset * 210)
         for month in range(1, 7)
         for offset, area in enumerate(["Bắc", "Trung", "Nam"], start=1)],
    )
    query = "SELECT month, region, revenue FROM sales"
    params = ()
    if region != "Tất cả":
        query += " WHERE region = ?"
        params = (region,)
    query += " ORDER BY month, region"
    data = pd.read_sql_query(query, connection, params=params)
finally:
    connection.close()

st.metric("Tổng doanh thu minh họa", f"{data.revenue.sum():,.0f}")
figure, axis = plt.subplots(figsize=(10, 4))
try:
    sns.lineplot(data=data, x="month", y="revenue", hue="region", marker="o", ax=axis)
    axis.set(xlabel="Tháng", ylabel="Doanh thu")
    figure.tight_layout()
    st.pyplot(figure)
finally:
    plt.close(figure)
st.dataframe(data, use_container_width=True, hide_index=True)
