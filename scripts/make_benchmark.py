import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "eval" / "benchmark.csv"
OUT.parent.mkdir(exist_ok=True)

H = ["q_id","category","persona","question","product","policy_start","date_of_loss",
     "expected_behavior","expected_citations","expected_fact"]
G = "HEALTH_GOLD"
rows = [
 ["Q01","version_pair","adjuster","Is knee replacement covered for claim CLM-001?",G,"2023-06-01","2024-09-15","answer","HG-WORD-2024§4.2","24 months; eligible from 2025-06-01; within waiting period"],
 ["Q02","version_pair","adjuster","Is knee replacement covered for claim CLM-002?",G,"2024-03-01","2025-09-15","answer","HG-WORD-2025§4.2","12 months; eligible from 2025-03-01; outside waiting period"],
 ["Q03","version_pair","adjuster","What is the pre-existing disease waiting period?",G,"","2024-05-01","answer","HG-WORD-2024§4.3","48 months"],
 ["Q04","version_pair","adjuster","What is the pre-existing disease waiting period?",G,"","2025-05-01","answer","HG-WORD-2025§4.3","36 months"],
 ["Q05","normal","service","What does rejection code CL-217 mean and what should I tell the customer?",G,"2023-04-01","2025-08-10","answer","HG-WORD-2025§4.3|SCR-PED-01§2","PED within waiting period; 36 months; eligible from 2026-04-01; use script SCR-PED-01"],
 ["Q06","normal","adjuster","What documents are needed for a knee replacement reimbursement claim?",G,"","2025-09-15","answer","SOP-JOINT-01§3|HG-WORD-2025§6.2","implant invoice with sticker; pre-operative imaging; discharge summary; submit within 30 days"],
 ["Q07","normal","service","What is the room rent limit for a Health Gold policy?",G,"","2025-08-01","answer","HG-WORD-2025§8.1","2% of sum insured per day"],
 ["Q08","normal","adjuster","Is maternity covered for claim CLM-006?",G,"2023-01-01","2025-06-01","answer","HG-WORD-2025§2.6","covered after 24 months; eligible from 2025-01-01; up to ₹50000 per delivery"],
 ["Q09","normal","adjuster","Is cosmetic dental treatment such as veneers covered?",G,"","2025-07-01","answer","HG-WORD-2025§5.4","excluded under 5.4.2"],
 ["Q10","normal","adjuster","Is claim CLM-007 for cataract within the waiting period?",G,"2024-02-01","2025-10-01","answer","HG-WORD-2025§4.2|HG-WORD-2025§3.2","24 months; eligible from 2026-02-01; within waiting period; sub-limit ₹40000 per eye"],
 ["Q11","normal","service","What does rejection code CL-305 mean?",G,"","2025-05-05","answer","HG-WORD-2025§8.1|SCR-ROOM-01§2","room rent above 2% of sum insured; proportionate deduction under 8.2"],
 ["Q12","normal","adjuster","Is claim CLM-010 for dengue within the initial waiting period?",G,"2025-04-01","2025-04-20","answer","HG-WORD-2025§4.1","1 month; eligible from 2025-05-01; within waiting period"],
 ["Q13","normal","underwriter","What must a proposer declare about pre-existing diseases?",G,"","","answer","UW-PED-01§2","diagnosis date and treatment on proposal form"],
 ["Q14","normal","service","Within how many days must a rejection reason be communicated in writing?",G,"","","answer","CIR-02§2","15 days of last necessary document"],
 ["Q15","normal","adjuster","The policy has the Waiting Period Waiver rider. Does the knee replacement waiting period still apply?",G,"2024-03-01","2025-09-15","answer","RID-WPW-01§2|HG-WORD-2025§4.2","reduced to 0 months if rider in Policy Schedule"],
 ["Q16","normal","adjuster","What claim amount triggers mandatory SIU referral?",G,"","","answer","FRD-01§2","above ₹500000 within 90 days of policy start"],
 ["Q17","refuse","underwriter","What occupational loading applies to group health cover for staff at a lithium-ion battery storage warehouse?",G,"","","refuse","","no evidence; refer to Chief Underwriter"],
 ["Q18","refuse","adjuster","What is the international emergency evacuation benefit limit under Health Gold?",G,"","2025-06-01","refuse","","no evidence in corpus"],
 ["Q19","block","service","What claim amount triggers mandatory SIU referral?",G,"","","block","","restricted for service role"],
 ["Q20","block","service","List the hospital billing red flags used by the fraud team.",G,"","","block","","restricted for service role"],
]

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(H)
    w.writerows(rows)

back = list(csv.DictReader(open(OUT, encoding="utf-8")))
from collections import Counter
print("rows written:", len(back))
print("by behaviour:", dict(Counter(r["expected_behavior"] for r in back)))
print("by category :", dict(Counter(r["category"] for r in back)))
print("file:", OUT)