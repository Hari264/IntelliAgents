import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.agent import run

def show(title, r):
    print("=" * 90); print(title)
    print("tools:", [t["tool"] for t in r["tools_called"]])
    print(f"tokens in/out: {r['tokens_in']}/{r['tokens_out']} | cost: ${r['cost_usd']}")
    print("-" * 90); print(r["answer"])

show("1. Knee, CLM-001 (loss 2024-09-15)",
     run("Is knee replacement covered, what is the waiting period, and does the loss fall inside it?",
         "adjuster", "2024-09-15", "2023-06-01"))
show("2. Knee, CLM-002 (loss 2025-09-15)",
     run("Is knee replacement covered, what is the waiting period, and does the loss fall inside it?",
         "adjuster", "2025-09-15", "2024-03-01"))
show("3. CL-217 for a service agent",
     run("What does rejection code CL-217 mean and what should I tell the customer?",
         "service", "2025-08-10", "2023-04-01"))
show("4. Li-ion warehouse (should refuse)",
     run("What occupational loading applies to group health cover for staff at a lithium-ion battery storage warehouse?",
         "underwriter"))