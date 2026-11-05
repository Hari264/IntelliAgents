import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app import refusals
from app.config import search

for r in refusals.list_refusals():
    print(f"#{r['id']} status={r['status']:<9} doc_id={r['doc_id']} persona={r['persona']}")

print("\napproved guidance in the index:")
for h in search.search("*", filter="doc_type eq 'approved_guidance'", select=["citation", "audience"]):
    print("  ", h["citation"], "audience =", list(h["audience"]))