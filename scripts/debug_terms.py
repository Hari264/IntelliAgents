import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.agent import run
from app.tools import search_clauses

cases = [
    ("Is knee replacement covered, what is the waiting period, and does the loss fall inside it?",
     "adjuster", "2024-09-15", "2023-06-01"),
    ("Is knee replacement covered, what is the waiting period, and does the loss fall inside it?",
     "adjuster", "2025-09-15", "2024-03-01"),
    ("What occupational loading applies to group health cover for staff at a lithium-ion battery storage warehouse?",
     "underwriter", None, None),
]
for q, persona, dol, ps in cases:
    r = run(q, persona, dol, ps)
    for t in r["tools_called"]:
        if t["tool"] == "search_clauses":
            terms = t["args"].get("key_terms", [])
            res = search_clauses(t["args"]["query"], persona, dol, key_terms=terms)
            print(f"{persona}{dol}: terms={terms} -> covered={res['covered']} missing={res['missing_terms']}")
    print("   answer starts:", r["answer"][:60].replace("\n", " "), "\n")