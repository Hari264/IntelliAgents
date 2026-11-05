import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app import agent

r = agent.run("Is claim CLM-007 for cataract within the waiting period?", "adjuster", "2025-10-01", "2024-02-01")
print(r["status"], r["tools_called"])
print(r["answer"])