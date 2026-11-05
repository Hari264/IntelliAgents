import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app import refusals
from app.publish import publish
from app.config import search

def check(name, cond): print(("PASS  " if cond else "FAIL  ") + name)

# drafted (not approved) items must not be publishable
drafted = refusals.list_refusals("drafted")
if drafted:
    try:
        publish(drafted[0]["id"])
        check("a drafted item cannot be published", False)
    except ValueError:
        check("a drafted item cannot be published", True)

approved = refusals.list_refusals("approved")
assert approved, "No approved items. Run scripts\\test_review.py first."
rid = approved[0]["id"]
r = publish(rid)
time.sleep(3)

hits = list(search.search("*", filter=f"doc_id eq '{r['doc_id']}'", select=["citation", "audience", "doc_type"]))
check("approved draft is now in the index (3 chunks)", len(hits) == 3)
check("doc_type is approved_guidance and audience is [underwriter]",
      all(h["doc_type"] == "approved_guidance" and list(h["audience"]) == ["underwriter"] for h in hits))
check("item status is now 'indexed'", refusals.get_refusal(rid)["status"] == "indexed")
print("\npublished:", r)