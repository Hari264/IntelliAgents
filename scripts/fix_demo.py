import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app import refusals
from app.publish import unpublish
from app.config import search

# remove every approved guidance document from the index
ids = {h["doc_id"] for h in search.search("*", filter="doc_type eq 'approved_guidance'", select=["doc_id"])}
for d in ids:
    print("removed", d, "->", unpublish(d), "chunks")

# put drafted/approved/indexed items back to 'open'
for r in refusals.list_refusals():
    if r["status"] in ("drafted", "approved", "indexed"):
        refusals.reset_item(r["id"])

# the service-role Li-ion question is not a real gap for that role
for r in refusals.list_refusals("open"):
    if r["persona"] == "service" and "lithium" in r["question"].lower():
        refusals.dismiss(r["id"], "SME Demo")

time.sleep(3)
for r in refusals.list_refusals():
    print(f"#{r['id']} status={r['status']} persona={r['persona']}")