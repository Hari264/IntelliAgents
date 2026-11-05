import csv, time
from datetime import datetime, timezone
from app.config import ROOT
from app.agent import run
from app import refusals

LOG = ROOT / "logs" / "usage.csv"
FIELDS = ["timestamp", "persona", "date_of_loss", "question", "status", "tools",
          "tokens_in", "tokens_out", "cost_usd", "latency_s"]

def ask(question, persona, date_of_loss=None, policy_start=None):
    t0 = time.time()
    r = run(question, persona, date_of_loss, policy_start)
    r["latency_s"] = round(time.time() - t0, 2)

    # A refusal means a knowledge gap: save it for the SME to review
    r["refusal_id"] = None
    if r["status"] == "refused":
        terms = next((t["args"].get("key_terms", []) for t in r["tools_called"]
                      if t["tool"] == "search_clauses"), [])
        r["refusal_id"] = refusals.log_refusal(question, persona, date_of_loss, terms)

    LOG.parent.mkdir(exist_ok=True)
    new_file = not LOG.exists()
    with open(LOG, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new_file:
            w.writeheader()
        w.writerow({
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "persona": persona, "date_of_loss": date_of_loss or "",
            "question": question[:200], "status": r["status"],
            "tools": "|".join(t["tool"] for t in r["tools_called"]),
            "tokens_in": r["tokens_in"], "tokens_out": r["tokens_out"],
            "cost_usd": r["cost_usd"], "latency_s": r["latency_s"]})
    return r