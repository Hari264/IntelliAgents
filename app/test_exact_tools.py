import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.tools import lookup_rejection_code, compute_waiting_period

def check(name, cond): print(("PASS  " if cond else "FAIL  ") + name)

r = lookup_rejection_code("cl-217")
check("CL-217 -> SCR-PED-01, clause 4.3", r["found"] and r["customer_script_id"] == "SCR-PED-01" and r["clause_ref"] == "4.3")
check("unknown code handled", lookup_rejection_code("CL-999")["found"] is False)

a = compute_waiting_period("joint_replacement", "2023-06-01", "2024-09-15")   # CLM-001
check("CLM-001: v2024, 24 months, eligible 2025-06-01, inside waiting period",
      a["version"] == "v2024" and a["waiting_months"] == 24 and a["eligible_from"] == "2025-06-01" and a["within_waiting_period"])
b = compute_waiting_period("joint_replacement", "2024-03-01", "2025-09-15")   # CLM-002
check("CLM-002: v2025, 12 months, eligible 2025-03-01, outside waiting period",
      b["version"] == "v2025" and b["waiting_months"] == 12 and b["eligible_from"] == "2025-03-01" and not b["within_waiting_period"])
c = compute_waiting_period("pre_existing_disease", "2023-04-01", "2025-08-10")  # CLM-003 / CL-217
check("CLM-003: v2025, 36 months, eligible 2026-04-01, inside waiting period",
      c["waiting_months"] == 36 and c["eligible_from"] == "2026-04-01" and c["within_waiting_period"])
d = compute_waiting_period("maternity", "2021-01-01", "2024-07-01")            # CLM-005
check("CLM-005: maternity not covered under v2024", d["covered"] is False and d["version"] == "v2024")
e = compute_waiting_period("maternity", "2023-01-01", "2025-06-01")            # CLM-006
check("CLM-006: maternity 24 months, eligible 2025-01-01, outside waiting period",
      e["waiting_months"] == 24 and e["eligible_from"] == "2025-01-01" and not e["within_waiting_period"])