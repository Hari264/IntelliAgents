from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

def patch(rel, pairs):
    p = ROOT / rel
    t = p.read_text(encoding="utf-8")
    for pattern, new in pairs:
        t, n = re.subn(pattern, new, t, flags=re.I)
        print(f"{rel}: {n} x  {pattern!r}")
    p.write_text(t, encoding="utf-8")

patch("data/docs/riders/RID-CI-01.md", [
    (r"initial waiting period of 90 days", "initial waiting period, as specified in the Policy Schedule,"),
    (r"within this 90-day period", "within this initial waiting period"),
    (r"within the 90-day waiting period", "within the initial waiting period"),
    (r"organ transplants?", "major surgical intervention"),
])
patch("data/docs/underwriting/UW-OCC-01.md", [
    (r"fire evacuation plan with regular drills", "fire emergency plan with regular fire drills"),
])