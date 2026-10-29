"""Luồng NumPy: dữ liệu thiết bị, kịch bản và ưu tiên kiểm tra."""
from pathlib import Path
import argparse
import csv
import hashlib
import sqlite3
import numpy as np


def luu_csv(path, header, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def thuc_hanh(db, output):
    # BƯỚC 1: mở đúng tệp và chỉ đọc dữ liệu nguồn.
    db = Path(db).resolve()
    if not db.is_file():
        raise FileNotFoundError(db)
    truoc = hashlib.sha256(db.read_bytes()).hexdigest()
    con = sqlite3.connect(db.as_uri() + "?mode=ro", uri=True)
    try:
        # BƯỚC 2: giữ một dòng trên mỗi thiết bị.
        rows = con.execute("""
            SELECT MaTB, TrangThai, GioHoatDong
            FROM ThietBi ORDER BY MaTB
        """).fetchall()
        alarm_rows = con.execute("""
            SELECT c.MaTB, COUNT(*)
            FROM CanhBao b
            JOIN DuLieuCamBien d ON d.MaDL=b.MaDL
            JOIN CamBien c ON c.MaCB=d.MaCB
            GROUP BY c.MaTB
        """).fetchall()
    finally:
        con.close()

    # BƯỚC 3: tạo các mảng cùng thứ tự thiết bị.
    ma = np.array([r[0] for r in rows], dtype=str)
    trang_thai = np.array([r[1] for r in rows], dtype=str)
    gio = np.array([r[2] for r in rows], dtype=float)
    if gio.size == 0 or not np.isfinite(gio).all():
        raise ValueError("Cần giờ hoạt động hữu hạn, không rỗng")
    bang_dem = dict(alarm_rows)
    dem = np.array([bang_dem.get(m, 0) for m in ma], float)
    print("Mã:", ma, "Giờ:", gio, "Cảnh báo:", dem)
    print("shape, ndim, size:", gio.shape, gio.ndim, gio.size)

    # BƯỚC 4: điều kiện Boolean và thống kê theo trạng thái.
    mask = (gio >= 800) & (gio <= 1300)
    nhan, so_luong = np.unique(trang_thai, return_counts=True)
    print("Từ 800 đến 1300 giờ:", ma[mask], gio[mask].sum())
    print("Trạng thái:", list(zip(nhan, so_luong)))
    print("Tổng, trung bình:", gio.sum(), gio.mean())

    # BƯỚC 5: broadcasting ba kịch bản giả định.
    them = np.array([0, 80, 160], dtype=float)
    kich_ban = gio[:, None] + them
    trung_binh = kich_ban.mean(axis=0)
    vuot_moc = np.count_nonzero(kich_ban >= 1000, axis=0)
    nhom = np.select(
        [kich_ban >= 1200, kich_ban >= 800],
        ["Cao", "Vua"], default="Thap"
    )
    print("Ma trận giờ:\n", kich_ban)
    print("Trung bình theo kịch bản:", trung_binh)
    print("Số thiết bị đạt 1000 giờ:", vuot_moc)

    # BƯỚC 6: chuẩn hóa riêng từng cột đặc trưng gốc.
    dac_trung = np.column_stack((gio, dem))
    min_cot = dac_trung.min(axis=0)
    do_rong = np.ptp(dac_trung, axis=0)
    mau_so = np.where(do_rong == 0, 1, do_rong)
    chuan = (dac_trung - min_cot) / mau_so
    print("Đặc trưng [giờ, số cảnh báo]:\n", dac_trung)
    print("Đã chuẩn hóa:\n", np.round(chuan, 3))

    # BƯỚC 7: điểm giả định và phân tích độ nhạy trọng số.
    trong_so = np.array([0.6, 0.4])
    diem = chuan @ trong_so
    thu_tu = np.argsort(-diem, kind="stable")
    trong_so_moi = np.array([0.3, 0.7])
    diem_moi = chuan @ trong_so_moi
    thu_tu_moi = np.argsort(-diem_moi, kind="stable")
    print("Thứ tự 0.6/0.4:", ma[thu_tu])
    print("Điểm:", np.round(diem[thu_tu], 3))
    print("Thứ tự 0.3/0.7:", ma[thu_tu_moi])

    # BƯỚC 8: lưu kết quả riêng bằng csv, không cần pandas.
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    luu_csv(output / "thiet_bi_numpy.csv",
            ["MaTB", "TrangThai", "Gio", "SoCanhBao"],
            zip(ma, trang_thai, gio, dem))
    luu_csv(output / "kich_ban_gio.csv",
            ["MaTB", "Them0", "Them80", "Them160"],
            ((m, *a) for m, a in zip(ma, kich_ban)))
    luu_csv(output / "xep_hang.csv",
            ["Hang", "MaTB", "Diem_06_04"],
            ((h, str(ma[i]), float(diem[i]))
             for h, i in enumerate(thu_tu, 1)))
    luu_csv(output / "so_sanh_trong_so.csv",
            ["MaTB", "Diem_06_04", "Diem_03_07"],
            zip(ma, diem, diem_moi))

    # BƯỚC 9: mốc kiểm chứng cho đúng tệp bài học.
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
    return ma, gio, kich_ban, chuan, diem


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    here = Path(__file__).resolve().parent
    parser.add_argument("--db", type=Path,
                        default=here / "Warehouse_Automation.db")
    parser.add_argument("--out", type=Path,
                        default=here / "ket_qua_numpy")
    args = parser.parse_args()
    thuc_hanh(args.db, args.out)
