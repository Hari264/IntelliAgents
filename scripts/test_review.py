import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app import refusals
from app.config import search

def check(name, cond): print(("PASS  " if cond else "FAIL  ") + name)

drafted = refusals.list_refusals("drafted")
assert drafted, "No drafted items. Run scripts\\test_drafts.py first."
rid = drafted[0]["id"]

try:
    refusals.approve(rid, "")
    check("approval without a reviewer name is refused", False)
except ValueError:
    check("approval without a reviewer name is refused", True)

refusals.approve(rid, "SME Demo", "Looks safe")
item = refusals.get_refusal(rid)
check("status is approved, with reviewer and time saved",
      item["status"] == "approved" and item["reviewer"] == "SME Demo" and item["reviewed_at"])

try:
    refusals.approve(rid, "SME Demo")
    check("an approved item cannot be approved twice", False)
except ValueError:
    check("an approved item cannot be approved twice", True)

check("approved draft is still NOT in the search index",
      len(list(search.search("*", filter=f"doc_id eq '{item['doc_id']}'"))) == 0)
print(f"\nitem #{rid} doc_id={item['doc_id']} status={item['status']} reviewer={item['reviewer']}")