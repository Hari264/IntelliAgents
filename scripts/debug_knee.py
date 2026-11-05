import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.agent import run
from app.tools import search_clauses, _term_in

Q = "Is knee replacement covered, what is the waiting period, and does the loss fall inside it?"
for label, dol, ps in [("2024 loss", "2024-09-15", "2023-06-01"),
                       ("2025 loss", "2025-09-15", "2024-03-01")]:
    print("=" * 80, "\n", label)
    r = run(Q, "adjuster", dol, ps)
    print("covered_flags:", r["covered_flags"], "| answer starts:", r["answer"][:40].replace("\n", " "))
    for t in r["tools_called"]:
        if t["tool"] != "search_clauses":
            continue
        terms = t["args"].get("key_terms", [])
        res = search_clauses(t["args"]["query"], "adjuster", dol, key_terms=terms)
        text = " ".join(e["content"].lower() for e in res["evidence"])
        print("query    :", t["args"]["query"])
        print("evidence :", [e["citation"] for e in res["evidence"]])
        for term in terms:
            print(f"   term {term!r:35} found = {_term_in(term.lower(), text)}")