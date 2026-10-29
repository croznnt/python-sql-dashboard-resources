"""Ba bài thực hành pandas trên database kho mô phỏng."""
from pathlib import Path
import argparse
import hashlib
import sqlite3
import pandas as pd


def luu_csv(frame, output, name):
    output.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output / name, index=False, encoding="utf-8-sig")


def bai_1(con, output):
    # Đọc có thứ tự, xem cấu trúc và kiểm tra kiểu số.
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

    # loc chọn dòng theo mặt nạ và cột theo tên.
    mask = devices["TrangThai"].eq("DangChay")
    columns = ["MaTB", "TenTB", "GioHoatDong"]
    running = devices.loc[mask, columns].copy()
    running = running.sort_values("MaTB")
    summary = devices["GioHoatDong"].agg(
        ["count", "sum", "mean", "median", "min", "max"]
    ).rename_axis("ChiTieu").reset_index(name="GiaTri")

    assert devices.shape == (4, 6)
    assert running["MaTB"].tolist() == ["BC01", "PLC01"]
    assert abs(devices["GioHoatDong"].sum() - 3980) < 1e-9
    assert abs(devices["GioHoatDong"].mean() - 995) < 1e-9
    print(running.to_string(index=False))
    print(summary.to_string(index=False))
    luu_csv(running, output, "bai01_dang_chay.csv")
    luu_csv(summary, output, "bai01_thong_ke_gio.csv")


def bai_2(con, output):
    # Đọc riêng từng bảng để thực hiện phép ghép bằng pandas.
    devices = pd.read_sql_query(
        "SELECT * FROM ThietBi ORDER BY MaTB", con
    )
    areas = pd.read_sql_query(
        "SELECT MaKV, TenKV FROM KhuVuc ORDER BY MaKV", con
    )
    tasks = pd.read_sql_query(
        "SELECT MaTV, MaTB FROM TacVuVanHanh ORDER BY MaTV", con
    )
    located = devices.merge(
        areas, on="MaKV", how="left",
        validate="many_to_one", indicator=True
    )
    if not located["_merge"].eq("both").all():
        raise ValueError("Thiết bị thiếu khu vực hợp lệ")
    located = located.drop(columns="_merge")
    by_area = located.groupby(
        ["MaKV", "TenKV"], as_index=False
    ).agg(
        SoThietBi=("MaTB", "size"),
        TongGio=("GioHoatDong", "sum"),
        GioTrungBinh=("GioHoatDong", "mean")
    ).sort_values("MaKV")

    # Tổng hợp bảng con trước, giữ một dòng trên mỗi thiết bị.
    task_count = tasks.groupby("MaTB", as_index=False).agg(
        SoTacVu=("MaTV", "size")
    )
    assigned = devices[["MaTB", "TenTB", "TrangThai"]].merge(
        task_count, on="MaTB", how="left", validate="one_to_one"
    )
    assigned["SoTacVu"] = assigned["SoTacVu"].fillna(0).astype("Int64")
    assigned = assigned.sort_values("MaTB")
    assert by_area["SoThietBi"].tolist() == [2, 1, 1]
    assert by_area["TongGio"].tolist() == [2060, 1500, 420]
    assert assigned["SoTacVu"].tolist() == [1, 1, 1, 0]
    assert int(assigned["SoTacVu"].sum()) == len(tasks)
    print(by_area.to_string(index=False))
    print(assigned.to_string(index=False))
    luu_csv(by_area, output, "bai02_khu_vuc.csv")
    luu_csv(assigned, output, "bai02_phan_cong.csv")


def bai_3(con, output):
    # read_sql_query truyền tham số riêng, không nối chuỗi SQL.
    readings = pd.read_sql_query(
        "SELECT * FROM DuLieuCamBien WHERE ThoiDiem >= ? ORDER BY MaDL",
        con, params=("2026-10-08 00:00:00",)
    )
    sensors = pd.read_sql_query(
        "SELECT * FROM CamBien ORDER BY MaCB", con
    )
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

    # Chỉ so với cận đã khai báo. NULL ở cận không phải số 0.
    low = data["NguongDuoi"].notna() & data["GiaTri"].lt(data["NguongDuoi"])
    high = data["NguongTren"].notna() & data["GiaTri"].gt(data["NguongTren"])
    data["VuotNguong"] = (low | high).astype("Int64")
    columns = ["MaDL", "MaCB", "MaTB", "ThoiDiem", "GiaTri", "DonVi"]
    abnormal = data.loc[data["VuotNguong"].eq(1), columns].copy()

    latest = data.sort_values(["ThoiDiem", "MaDL"]).groupby(
        "MaCB", sort=False
    ).tail(1).sort_values("MaCB")
    if data.duplicated(["ThoiDiem", "MaCB"]).any():
        raise ValueError("Cần quy tắc xử lý mẫu trùng trước pivot")
    matrix = data.pivot(
        index="ThoiDiem", columns="MaCB", values="GiaTri"
    ).sort_index().rename_axis(columns=None).reset_index()

    assert len(data) == 6
    assert abnormal["MaDL"].tolist() == [2, 5]
    assert latest["GiaTri"].tolist() == [68, 1, 18, 2.1]
    assert matrix.shape == (2, 5)
    assert int(matrix.drop(columns="ThoiDiem").isna().sum().sum()) == 2
    print(abnormal.to_string(index=False))
    print(matrix.to_string(index=False))
    luu_csv(abnormal, output, "bai03_vuot_nguong.csv")
    luu_csv(latest[columns + ["VuotNguong"]], output, "bai03_moi_nhat.csv")
    luu_csv(matrix, output, "bai03_ma_tran.csv")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    here = Path(__file__).resolve().parent
    parser.add_argument("--db", type=Path, default=here / "Warehouse_Automation.db")
    parser.add_argument("--out", type=Path, default=here / "ket_qua_pandas")
    parser.add_argument("--bai", choices=["all", "1", "2", "3"], default="all")
    args = parser.parse_args()
    db = args.db.resolve()
    if not db.is_file():
        raise FileNotFoundError(db)
    before = hashlib.sha256(db.read_bytes()).hexdigest()
    con = sqlite3.connect(db.as_uri() + "?mode=ro", uri=True)
    try:
        for key, fn in [("1", bai_1), ("2", bai_2), ("3", bai_3)]:
            if args.bai in ("all", key):
                fn(con, args.out)
    finally:
        con.close()
    assert before == hashlib.sha256(db.read_bytes()).hexdigest()
    print("Kiểm chứng thành công, database nguồn giữ nguyên.")


if __name__ == "__main__":
    main()
