import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.service import ask
from app.config import search

def check(name, cond): print(("PASS  " if cond else "FAIL  ") + name)

LIION = "What occupational loading applies to group health cover for staff at a lithium-ion battery storage warehouse?"

ids = [h["citation"] for h in search.search("*", filter="doc_id eq 'APPR-001'", select=["citation"])]
assert ids, "APPR-001 is not in the index. Run scripts\\test_publish.py first."

time.sleep(2)
under = ask(LIION, "underwriter")
svc   = ask(LIION, "service")

check("underwriter: answered", under["status"] == "answered")
check("underwriter: cites APPR-001", "APPR-001§" in under["answer"])
check("underwriter: mentions the Chief Underwriter", "chief underwriter" in under["answer"].lower())
check("underwriter: no percentage invented", "%" not in under["answer"])
check("service role does NOT get the guidance (approved for underwriter only)", svc["status"] == "refused")

print(f"\ncost: ${under['cost_usd']} | latency: {under['latency_s']}s")
print("\n----- underwriter answer -----\n" + under["answer"])