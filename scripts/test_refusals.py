import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.service import ask
from app import refusals

def check(name, cond): print(("PASS  " if cond else "FAIL  ") + name)

LIION = "What occupational loading applies to group health cover for staff at a lithium-ion battery storage warehouse?"

a = ask(LIION, "underwriter")
b = ask(LIION, "underwriter")            # same question again
k = ask("Is knee replacement covered, what is the waiting period, and does the loss fall inside it?",
        "adjuster", "2025-09-15", "2024-03-01")
f = ask("What claim amount triggers mandatory SIU referral?", "service", "2025-09-15")

check("Li-ion was refused and got a refusal id", a["status"] == "refused" and a["refusal_id"])
check("asking again reuses the same id (no duplicate)", a["refusal_id"] == b["refusal_id"])
check("an answered question is not logged", k["status"] == "answered" and k["refusal_id"] is None)
check("a blocked question is not logged", f["status"] == "blocked" and f["refusal_id"] is None)

item = refusals.get_refusal(a["refusal_id"])
check("item is open with the persona and key terms saved",
      item["status"] == "open" and item["persona"] == "underwriter" and item["key_terms"] != "")
check("exactly one open Li-ion item in the log",
      sum(1 for r in refusals.list_refusals("open") if "lithium" in r["question"]) == 1)

print("\nopen items:")
for r in refusals.list_refusals("open"):
    print(f"  #{r['id']} [{r['persona']}] terms=({r['key_terms']}) {r['question'][:60]}")