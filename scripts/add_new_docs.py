import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ZIP = Path.home() / "Downloads" / "data 1.zip"      # change this if your zip is somewhere else

if not ZIP.exists():
    raise SystemExit(f"Zip not found: {ZIP}\nEdit the ZIP line at the top of this script.")

added, skipped = [], 0
with zipfile.ZipFile(ZIP) as z:
    names = z.namelist()
    for name in names:
        if not name.endswith(".md") or "data/docs/" not in name:
            continue
        rel = name.split("data/docs/", 1)[1]                 # e.g. sops/SOP-NETWORK-01.md
        dest = ROOT / "data" / "docs" / rel
        if dest.exists():
            skipped += 1
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(z.read(name))
        added.append(rel)
    print("benchmark_extra.csv in the zip:", any(n.endswith("benchmark_extra.csv") for n in names))

for rel in added:
    print("added", rel)
print(f"\nadded {len(added)}, skipped (already existed) {skipped}")
print("total .md files now:", len(list((ROOT / "data" / "docs").rglob("*.md"))))