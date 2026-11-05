import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.evidence_pack import build_pack

def check(name, cond): print(("PASS  " if cond else "FAIL  ") + name)

p24 = build_pack("joint_replacement", "adjuster", "2023-06-01", "2024-09-15")
p25 = build_pack("joint_replacement", "adjuster", "2024-03-01", "2025-09-15")

check("2024 pack: ok, 24 months, eligible 2025-06-01, inside",
      p24["status"] == "ok" and "24 months" in p24["pack"] and "2025-06-01" in p24["pack"] and "falls inside" in p24["pack"])
check("2024 pack: no 2025 document cited", "HG-WORD-2025" not in p24["pack"] and "RID-WPW-01" not in p24["pack"])
check("2025 pack: 12 months, eligible 2025-03-01, outside",
      "12 months" in p25["pack"] and "2025-03-01" in p25["pack"] and "falls outside" in p25["pack"])
check("2025 pack: waiver rider listed under exceptions", "RID-WPW-01" in p25["pack"])
check("both packs: sub-limit ₹3,00,000 and room rent shown", "₹3,00,000" in p25["pack"] and "% of sum insured" in p24["pack"])
check("both packs: an SOP step is listed", "SOP-JOINT-01" in p24["pack"] and "SOP-JOINT-01" in p25["pack"])
check("guard finds no problems in either pack", p24["problems"] == [] and p25["problems"] == [])

check("2025 pack: waiver benefit clause RID-WPW-01§2 included", "RID-WPW-01§2" in p25["pack"])
check("packs: irrelevant rejection-letter SOP removed", "SOP-REJCOMM-01" not in p24["pack"] and "SOP-REJCOMM-01" not in p25["pack"])
check("2025 pack: excerpt shows the joint replacement sentence", "4.2.1 Joint replacement" in p25["pack"])

print("\ncost per pack: $", p25["cost_usd"], "| tokens:", p25["tokens"])

print("problems:", p24["problems"], p25["problems"])
print("\n" + p25["pack"])