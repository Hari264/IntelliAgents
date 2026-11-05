import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app import refusals
from app.publish import unpublish
from app.service import ask

LIION = "What occupational loading applies to group health cover for staff at a lithium-ion battery storage warehouse?"

removed = 0
for r in refusals.list_refusals():
    if r["doc_id"]:
        removed += unpublish(r["doc_id"])        # take the approved guidance out of the index
        refusals.reset_item(r["id"])             # back to 'open'
print("chunks removed from the index:", removed)

import time; time.sleep(3)
r = ask(LIION, "underwriter")
print("Li-ion question now ->", r["status"])
print("open items:", [(x["id"], x["status"]) for x in refusals.list_refusals("open")])