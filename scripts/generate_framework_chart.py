"""Generate a framework distribution chart from the local catalog."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

ROOT = Path(__file__).resolve().parents[1]
FRAMEWORKS = {
    "Streamlit": "Streamlit",
    "Dash": "Dash",
    "Panel": "Panel",
    "NiceGUI": "NiceGUI",
    "Superset": "apache/superset",
}


def classify(rows):
    groups = {name: [] for name in FRAMEWORKS}
    for row in rows:
        tokens = {token.strip().casefold() for token in row["stack"].split(",")}
        for name, marker in FRAMEWORKS.items():
            if marker.casefold() in tokens or row["repository"] == marker:
                groups[name].append(row["repository"])
    return groups


def main():
    rows = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    groups = classify(rows)
    names = sorted(groups, key=lambda name: -len(groups[name]))
    values = [len(groups[name]) for name in names]
    covered = len({repo for repos in groups.values() for repo in repos})
    output = ROOT / "assets"
    output.mkdir(exist_ok=True)
    with plt.rc_context({"font.family": "DejaVu Sans", "font.size": 11}):
        figure, axis = plt.subplots(figsize=(11, 5.8), facecolor="#f8fafc")
        axis.set_facecolor("#f8fafc")
        bars = axis.barh(names, values, color=["#2563eb", "#7c3aed", "#0891b2", "#059669", "#d97706"], height=0.58)
        axis.invert_yaxis()
        axis.bar_label(bars, labels=[f"{n} repo" for n in values], padding=10, fontsize=12)
        axis.set_xlim(0, max(values) + 0.8)
        axis.xaxis.set_major_locator(MaxNLocator(integer=True))
        axis.set_xlabel("Số repo trong danh mục", labelpad=12)
        axis.set_axisbelow(True)
        axis.grid(axis="x", color="#e2e8f0")
        axis.tick_params(axis="both", length=0)
        for spine in axis.spines.values():
            spine.set_visible(False)
        figure.text(0.07, 0.93, "PHÂN BỐ REPO THEO FRAMEWORK", fontsize=19, weight="bold", color="#0f172a")
        figure.text(0.07, 0.87, "Framework giao diện và nền tảng BI được ghi nhận trong catalog.json", color="#475569")
        figure.text(0.07, 0.075, f"{covered}/{len(rows)} repo thuộc các nhóm trên · {len(rows) - covered} repo thư viện/cơ sở dữ liệu được loại khỏi biểu đồ", fontsize=10, color="#475569")
        figure.text(0.07, 0.035, "Tính theo trường stack; Superset nhận diện bằng tên repo. Không suy diễn từ ghi chú đề xuất.", fontsize=9, color="#64748b")
        figure.subplots_adjust(left=0.15, right=0.94, top=0.79, bottom=0.22)
        figure.savefig(output / "framework-distribution.png", dpi=180, facecolor=figure.get_facecolor())
        figure.savefig(output / "framework-distribution.svg", facecolor=figure.get_facecolor())
        plt.close(figure)
    (output / "framework-counts.json").write_text(
        json.dumps({"total_repositories": len(rows), "covered_repositories": covered,
                    "excluded_repositories": len(rows) - covered, "groups": groups},
                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({name: len(groups[name]) for name in names}, ensure_ascii=False))


if __name__ == "__main__":
    main()
