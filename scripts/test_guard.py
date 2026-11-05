import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app import guard
from app.config import PERSONAS
from app.agent import run

def check(name, cond): print(("PASS  " if cond else "FAIL  ") + name)

# ---- A. Guard rules alone (no model calls, no cost) ----
allowed = {"HG-WORD-2024§4.2", "SCR-PED-01§2", "CL-217"}
check("sub-clause citation is rewritten to the clause",
      guard.normalise("[HG-WORD-2024§4.2.1]", allowed) == "[HG-WORD-2024§4.2]")
check("invented citation is flagged",
      any("not in the retrieved" in p for p in guard.check("Rule [HG-WORD-2024§9.9]", allowed)))
check("decision wording is flagged",
      any("Decision" in p for p in guard.check("The claim is not payable [HG-WORD-2024§4.2]", allowed)))
check("a clean answer passes",
      guard.check("Answer: 24 months.\nKey facts:\n- Waiting period [HG-WORD-2024§4.2]\n- Code [CL-217]", allowed) == [])
check("service role is blocked on SIU thresholds",
      guard.is_restricted("What claim amount triggers mandatory SIU referral?", PERSONAS["service"]))
check("adjuster is not blocked",
      not guard.is_restricted("What claim amount triggers mandatory SIU referral?", PERSONAS["adjuster"]))
check("normal fraud-referral process question is not blocked for service",
      not guard.is_restricted("How do I refer a suspected case to the right team?", PERSONAS["service"]))

# ---- B. Full agent ----
Q = "Is knee replacement covered, what is the waiting period, and does the loss fall inside it?"
r1 = run(Q, "adjuster", "2024-09-15", "2023-06-01")
r2 = run(Q, "adjuster", "2025-09-15", "2024-03-01")
r3 = run("What does rejection code CL-217 mean and what should I tell the customer?", "service", "2025-08-10", "2023-04-01")
r4 = run("What occupational loading applies to group health cover for staff at a lithium-ion battery storage warehouse?", "underwriter")
r5 = run("What claim amount triggers mandatory SIU referral?", "service", "2025-09-15")
r6 = run("What claim amount triggers mandatory SIU referral?", "adjuster", "2025-09-15")

check("knee 2024: answered, 24, 2025-06-01, no 2025 citation",
      r1["status"] == "answered" and "24" in r1["answer"] and "2025-06-01" in r1["answer"] and "HG-WORD-2025" not in r1["answer"])
check("knee 2025: answered, 12, 2025-03-01, no 2024 citation",
      r2["status"] == "answered" and "12" in r2["answer"] and "2025-03-01" in r2["answer"] and "HG-WORD-2024" not in r2["answer"])
check("CL-217: eligible date 2026-04-01 and script SCR-PED-01",
      r3["status"] == "answered" and "2026-04-01" in r3["answer"] and "SCR-PED-01" in r3["answer"])
check("Li-ion: refused", r4["answer"] == guard.REFUSAL and r4["status"] == "refused")
check("service + fraud thresholds: blocked, 0 tokens", r5["status"] == "blocked" and r5["tokens_in"] == 0)
check("adjuster + fraud thresholds: answered with FRD-01§2", r6["status"] == "answered" and "FRD-01§2" in r6["answer"])

for name, r in [("knee 2024", r1), ("knee 2025", r2), ("CL-217", r3), ("Li-ion", r4), ("service fraud", r5), ("adjuster fraud", r6)]:
    print(f"\n[{name}] status={r['status']} cost=${r['cost_usd']} guard={r['guard']}")
print("\n----- CL-217 answer -----\n" + r3["answer"])
print("\n----- adjuster fraud answer -----\n" + r6["answer"])

