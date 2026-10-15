"""Embed current catalog into the standalone interactive chart. No dependencies."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
data = json.loads((root / "catalog.json").read_text(encoding="utf-8"))
page = root / "docs/index.html"
text = page.read_text(encoding="utf-8")
start = text.index("// DATA_START")
end = text.index("// DATA_END")
payload = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
text = text[:start] + "// DATA_START\nconst catalog = " + payload + ";\n" + text[end:]
page.write_text(text, encoding="utf-8")
print(f"Embedded {len(data)} repositories into docs/index.html")
