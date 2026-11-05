import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app import refusals

refusals.reset_item(1)          # back to 'open', draft and review cleared
for r in refusals.list_refusals():
    print(f"#{r['id']} status={r['status']} persona={r['persona']} | {r['question'][:50]}")