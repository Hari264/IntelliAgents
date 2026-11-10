import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app import agent

for i in range(3):                       # run 3 times, because the model's choices vary
    r = agent.run("Is claim CLM-010 for dengue within the initial waiting period?",
                  "adjuster", "2025-04-20", "2025-04-01")
    terms = [t["args"].get("key_terms") for t in r["tools_called"] if t["tool"] == "search_clauses"]
    print(f"run {i+1}: status={r['status']} tools={[t['tool'] for t in r['tools_called']]} key_terms={terms}")
    for t in agent.LAST_TOOL_RESULTS:
        if t["tool"] == "search_clauses":
            print("   covered:", t["result"]["covered"], "| missing:", t["result"]["missing_terms"])