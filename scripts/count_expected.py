import re, yaml
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
FRONT = re.compile(r"^\ufeff?---\s*\n(.*?)\n---\s*\n(.*)$", re.S)
HEAD = re.compile(r"^## (Clause|Section) \d+", re.M)

docs, by_type, chunks, fraud, silver = 0, Counter(), 0, 0, []
for p in sorted((ROOT / "data" / "docs").rglob("*.md")):
    m = FRONT.match(p.read_text(encoding="utf-8"))
    meta = yaml.safe_load(m.group(1))
    n = len(HEAD.findall(m.group(2)))
    docs += 1
    chunks += n
    by_type[meta["doc_type"]] += n
    if meta["doc_type"] == "fraud_playbook":
        fraud += n
    if meta["product"] == "HEALTH_SILVER":
        silver.append(meta["doc_id"])

print("documents :", docs)
print("chunks    :", chunks)
print("fraud chunks:", fraud)
print("by doc_type:", dict(by_type))
print("silver docs:", silver)