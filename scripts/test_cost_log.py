import sys, csv
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.service import ask, LOG

def check(name, cond): print(("PASS  " if cond else "FAIL  ") + name)

before = sum(1 for _ in open(LOG, encoding="utf-8")) - 1 if LOG.exists() else 0

ask("Is knee replacement covered, what is the waiting period, and does the loss fall inside it?",
    "adjuster", "2025-09-15", "2024-03-01")
ask("What claim amount triggers mandatory SIU referral?", "service", "2025-09-15")
ask("What occupational loading applies to staff at a lithium-ion battery storage warehouse?", "underwriter")

rows = list(csv.DictReader(open(LOG, encoding="utf-8")))
new = rows[before:]
check("3 new rows were logged", len(new) == 3)
check("statuses are answered / blocked / refused", [r["status"] for r in new] == ["answered", "blocked", "refused"])
check("blocked question cost $0", float(new[1]["cost_usd"]) == 0)
check("every row has a latency", all(float(r["latency_s"]) >= 0 for r in new))

paid = [float(r["cost_usd"]) for r in new if r["status"] != "blocked"]
print(f"\naverage cost per model-answered question: ${sum(paid)/len(paid):.5f}")
for r in new:
    print(f"{r['status']:<9} ${r['cost_usd']:<8}{r['latency_s']}s  {r['question'][:55]}")