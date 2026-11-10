import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app import agent

CASES = [
    ("Q02", "Is knee replacement covered for claim CLM-002?", "adjuster", "2025-09-15", "2024-03-01"),
    ("Q11", "What does rejection code CL-305 mean?", "service", "2025-05-05", None),
]
for qid, q, persona, dol, ps in CASES:
    r = agent.run(q, persona, dol, ps)
    print("=" * 80)
    print(qid, "| status:", r["status"], "| covered_flags:", r["covered_flags"])
    print("tools:", [t["tool"] for t in r["tools_called"]])
    for t in agent.LAST_TOOL_RESULTS:
        res = t["result"]
        if t["tool"] == "search_clauses":
            print("  key_terms sent :", [x["args"].get("key_terms") for x in r["tools_called"] if x["tool"] == "search_clauses"])
            print("  covered        :", res["covered"], "| missing:", res["missing_terms"])
            print("  evidence       :", [e["citation"] for e in res["evidence"]])
        else:
            print(" ", t["tool"], "->", json.dumps(res, default=str)[:160])