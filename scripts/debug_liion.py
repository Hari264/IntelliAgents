import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.agent import run
from app.tools import search_clauses

q = "What occupational loading applies to group health cover for staff at a lithium-ion battery storage warehouse?"
r = run(q, "underwriter")

print("TOOL CALLS THE MODEL MADE:")
for t in r["tools_called"]:
    print(json.dumps(t, indent=2))

terms = next((t["args"].get("key_terms") for t in r["tools_called"] if t["tool"] == "search_clauses"), [])
res = search_clauses(q, "underwriter", key_terms=terms)
print("\nkey_terms the model sent:", terms)
print("covered:", res["covered"], "| missing:", res["missing_terms"])