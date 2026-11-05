import re
import sys
from datetime import date
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from app.service import ask
from app.config import PERSONAS
from app.evidence_pack import build_pack, CONDITION_TERMS
from app import refusals

st.set_page_config(page_title="ClaimsIQ", page_icon="🩺", layout="wide")
LABELS = {"service": "Service Agent", "adjuster": "Claims Adjuster", "underwriter": "Underwriter"}
BADGE = {"answered": ("✅ Answered", st.success), "refused": ("⚠️ Refused: not enough evidence", st.warning),
         "blocked": ("⛔ Blocked: restricted for your role", st.error)}
ICON = {"open": "🟠", "drafted": "📝", "approved": "🟢", "indexed": "✅", "rejected": "⚪"}

for key, default in [("history", []), ("pack", None), ("warn", {})]:
    if key not in st.session_state:
        st.session_state[key] = default

def draft_warnings(text):
    w = []
    if "%" in text:
        w.append("The draft contains a percentage. Check it is not assigned by analogy.")
    if re.search(r"consistent with class|falls? (under|into) class|attract", text, re.I):
        w.append("The draft may assign a class by analogy.")
    if "chief underwriter" not in text.lower():
        w.append("The draft does not mention the Chief Underwriter (expected for underwriting gaps).")
    return w

# ================= PAGE: refusal log =================
def log_page():
    st.header("Refusal log: SME review")
    st.caption("Every refused question is a knowledge gap. Nothing reaches the search index until a person approves it.")
    reviewer = st.text_input("Reviewer name", value="SME Demo")
    items = refusals.list_refusals()
    if not items:
        st.info("No refusals yet. Ask a question the knowledge base cannot answer.")
        return
    for it in reversed(items):
        rid, status = it["id"], it["status"]
        title = f"{ICON.get(status, '')} #{rid} [{status}] {LABELS.get(it['persona'], it['persona'])}: {it['question'][:75]}"
        with st.expander(title, expanded=status in ("open", "drafted", "approved")):
            st.write(it["question"])
            st.caption(f"Role: {it['persona']} | key terms: {it['key_terms'] or '-'} | logged {it['created_at']}")

            if status == "open":
                c1, c2 = st.columns(2)
                if c1.button("Draft guidance with AI", key=f"draft{rid}"):
                    from app.drafts import make_draft
                    with st.spinner("Drafting..."):
                        try:
                            d = make_draft(rid)
                            st.session_state.warn[rid] = d["problems"] + (
                                [f"New numbers not in the reference: {d['new_numbers']}"] if d["new_numbers"] else [])
                        except Exception as e:
                            st.error(str(e))
                    st.rerun()
                if c2.button("Dismiss (not a real gap)", key=f"dis{rid}"):
                    refusals.dismiss(rid, reviewer)
                    st.rerun()

            elif status == "drafted":
                parts = it["draft"].split("---", 2)
                st.info(f"Once published, this will be visible ONLY to the **{LABELS.get(it['persona'], it['persona'])}** role.")
                st.caption(f"Proposed document {it['doc_id']} | audience and type are set by the system, not the AI")
                st.markdown(parts[2] if len(parts) == 3 else it["draft"])
                for w in st.session_state.warn.get(rid, []) + draft_warnings(it["draft"]):
                    st.warning(w)
                c1, c2 = st.columns(2)
                if c1.button("✅ Approve", key=f"app{rid}"):
                    try:
                        refusals.approve(rid, reviewer)
                    except ValueError as e:
                        st.error(str(e))
                    st.rerun()
                if c2.button("❌ Reject", key=f"rej{rid}"):
                    try:
                        refusals.reject(rid, reviewer)
                    except ValueError as e:
                        st.error(str(e))
                    st.rerun()

            elif status == "approved":
                st.success(f"Approved by {it['reviewer']} at {it['reviewed_at']}. Not searchable yet.")
                if st.button("Publish to the search index", key=f"pub{rid}"):
                    from app.publish import publish
                    with st.spinner("Embedding and uploading..."):
                        try:
                            r = publish(rid)
                            st.session_state.warn[rid] = []
                            st.success(f"Published {r['chunks']} chunks: {', '.join(r['citations'])}")
                        except Exception as e:
                            st.error(str(e))
                    st.rerun()

            elif status == "indexed":
                st.success(f"Published as {it['doc_id']} (approved by {it['reviewer']}). Ask the question again on the Ask page.")
            else:
                st.caption(f"Closed by {it['reviewer']} at {it['reviewed_at']}.")

# ================= sidebar =================
page = st.sidebar.radio("Page", ["Ask", "Refusal log (SME)"])
if page != "Ask":
    log_page()
    st.stop()

with st.sidebar:
    st.title("🩺 ClaimsIQ")
    st.caption("Governed claims knowledge assistant (PoC, synthetic data)")
    persona = st.selectbox("Role", list(PERSONAS), format_func=lambda p: LABELS.get(p, p))
    use_dates = st.checkbox("Claim dates known", value=True)
    date_of_loss = policy_start = None
    if use_dates:
        dl = st.date_input("Date of loss", value=date(2025, 9, 15))
        ps = st.date_input("Policy start date", value=date(2024, 3, 1))
        date_of_loss, policy_start = dl.isoformat(), ps.isoformat()
    st.caption("The date of loss decides which policy version applies. "
               "The role decides which documents you may see.")

    st.divider()
    st.subheader("Evidence pack")
    condition = st.selectbox("Condition", list(CONDITION_TERMS),
                             format_func=lambda c: c.replace("_", " "))
    if st.button("Build evidence pack"):
        if not (date_of_loss and policy_start):
            st.warning("Tick 'Claim dates known' and enter both dates first.")
        else:
            with st.spinner("Building the pack..."):
                try:
                    st.session_state.pack = build_pack(condition, persona, policy_start, date_of_loss)
                except Exception as e:
                    st.session_state.pack = {"status": "error", "reason": str(e)}

    st.divider()
    if st.button("Clear conversation"):
        st.session_state.history = []
        st.session_state.pack = None
        st.rerun()

st.header("Ask ClaimsIQ")

pk = st.session_state.pack
if pk:
    with st.expander("📋 Evidence pack", expanded=True):
        if pk["status"] == "ok":
            st.markdown(pk["pack"])
            st.download_button("Download pack (.md)", pk["pack"], file_name="evidence_pack.md")
            if pk["problems"]:
                st.warning("Guard warnings: " + "; ".join(pk["problems"]))
            else:
                st.caption(f"Guard check passed | {len(pk['citations'])} citations | embedding cost ${pk['cost_usd']}")
        else:
            st.warning(pk.get("reason") or "Could not build the pack.")

for item in st.session_state.history:
    with st.chat_message("user"):
        st.write(item["question"])
        st.caption(f"{LABELS.get(item['persona'])} | loss {item['dol'] or '-'} | start {item['ps'] or '-'}")
    with st.chat_message("assistant"):
        label, box = BADGE[item["status"]]
        box(label)
        if item["status"] == "answered":
            st.markdown(item["answer"])
        st.caption(f"tools: {item['tools'] or 'none'} | tokens {item['tin']}/{item['tout']} | "
                   f"cost ${item['cost']} | {item['latency']}s")

q = st.chat_input("Ask about a clause, a rejection code, a waiting period...")
if q:
    with st.spinner("Searching the knowledge base..."):
        r = ask(q, persona, date_of_loss, policy_start)
    st.session_state.history.append({
        "question": q, "persona": persona, "dol": date_of_loss, "ps": policy_start,
        "status": r["status"], "answer": r["answer"],
        "tools": ", ".join(t["tool"] for t in r["tools_called"]),
        "tin": r["tokens_in"], "tout": r["tokens_out"], "cost": r["cost_usd"], "latency": r["latency_s"]})
    st.rerun()