import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app import agent

r = agent.run("What is the pre-existing disease waiting period?", "adjuster", "2024-05-01", None)
print("status:", r["status"], "| tokens:", r["tokens_in"], "/", r["tokens_out"])
print("tools called:", [t["tool"] for t in r["tools_called"]])
print("covered_flags:", r["covered_flags"])
for t in agent.LAST_TOOL_RESULTS:
    print(t["tool"], "->", json.dumps(t["result"], default=str)[:200])