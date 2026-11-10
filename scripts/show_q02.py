import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app import agent

for i in range(2):
    r = agent.run("Is knee replacement covered for claim CLM-002?", "adjuster", "2025-09-15", "2024-03-01")
    print(f"--- run {i+1}: {r['status']} tools={[t['tool'] for t in r['tools_called']]}")
    print(r["answer"][:700])