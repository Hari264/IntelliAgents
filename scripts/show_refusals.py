import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app import refusals
from app.config import search

for r in refusals.list_refusals():
    print(f"#{r['id']} status={r['status']:<9} doc_id={r['doc_id']} reviewer={r['reviewer']} | {r['question'][:55]}")

hits = list(search.search("*", filter="doc_id eq 'APPR-001'", select=["citation"]))
print("\nAPPR-001 chunks in the search index:", [h["citation"] for h in hits])