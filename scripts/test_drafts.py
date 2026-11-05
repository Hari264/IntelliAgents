import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app import refusals
from app.drafts import make_draft
from app.config import search

def check(name, cond): print(("PASS  " if cond else "FAIL  ") + name)

pending = refusals.list_refusals("open") + refusals.list_refusals("drafted")
assert pending, "No open or drafted items. Run scripts\\test_refusals.py first to log the Li-ion refusal."
rid = pending[0]["id"]
d = make_draft(rid)
item = refusals.get_refusal(rid)
text = d["markdown"].lower()

check("status is now 'drafted'", item["status"] == "drafted" and item["doc_id"] == d["doc_id"])
check("3-5 sections and no structure problems", d["problems"] == [] and 3 <= d["sections"] <= 5)
check("draft mentions lithium and battery", "lithium" in text and "battery" in text)
check("no invented percentages, amounts or periods", d["new_numbers"] == [])
check("draft is NOT in the search index",
      len(list(search.search("*", filter=f"doc_id eq '{d['doc_id']}'"))) == 0)

check("draft assigns no percentage and no class", "%" not in text and "consistent with class" not in text)
check("draft refers to the Chief Underwriter", "chief underwriter" in text)

print(f"\ncost: ${d['cost_usd']} | reference used: {d['reference']}")
print("new numbers to check:", d["new_numbers"])
print("\n" + d["markdown"])