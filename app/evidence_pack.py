import re
from app.config import aoai, EMBED_MODEL, PERSONAS
from app import tools, guard

# condition -> distinctive words that must appear in a clause for it to be relevant
CONDITION_TERMS = {
    "joint_replacement": ["joint replacement"], "pre_existing_disease": ["pre-existing"],
    "cataract": ["cataract"], "hernia": ["hernia"], "bariatric_surgery": ["bariatric"],
    "maternity": ["maternity"], "initial_waiting": ["waiting period"],
}
# condition -> the SOP written for it (used first when it exists)
CONDITION_SOP = {"joint_replacement": "SOP-JOINT-01", "pre_existing_disease": "SOP-PEDVER-01"}

def inr(n):
    """Indian digit grouping: 300000 -> ₹3,00,000"""
    s = str(int(n)); head, tail = s[:-3], s[-3:]; parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:]); head = head[:-2]
    if head:
        parts.insert(0, head)
    return "₹" + ",".join(parts + [tail])

def _excerpt(content, terms=None, n=260):
    """Show the paragraph that mentions the condition (e.g. '4.2.1 Joint replacement...'), not just the clause start."""
    body = re.sub(r"^## .*\n+", "", content.strip())
    paras = [p.strip() for p in body.splitlines() if p.strip()]
    pick = None
    if terms:
        pick = next((p for p in paras if any(tools._term_in(t, p.lower()) for t in terms)), None)
    text = " ".join((pick or " ".join(paras)).split())
    return text if len(text) <= n else text[:n].rsplit(" ", 1)[0] + " ..."

def _num(citation):
    return int(citation.split("§")[1].split(".")[0])

def _fetch(vec, query, persona, d, product, doc_type, top):
    aud = " or ".join(f"a eq '{a}'" for a in PERSONAS[persona])
    flt = (f"product eq '{product}' and effective_from le {d}T00:00:00Z and effective_to ge {d}T00:00:00Z "
           f"and audience/any(a: {aud}) and doc_type eq '{doc_type}'")
    return tools._search(query, vec, flt, top)

def build_pack(condition, persona, policy_start, date_of_loss, product="HEALTH_GOLD"):
    terms = CONDITION_TERMS[condition]
    calc = tools.compute_waiting_period(condition, policy_start, date_of_loss, product)
    if not calc.get("ok"):
        return {"status": "refused", "pack": None, "reason": calc.get("message")}

    query = f"{condition.replace('_', ' ')} waiting period sub-limit exceptions documents"
    emb = aoai.embeddings.create(model=EMBED_MODEL, input=query)
    vec = emb.data[0].embedding
    keep = lambda rows: [r for r in rows if any(tools._term_in(t, r["content"].lower()) for t in terms)]

    wording = keep(_fetch(vec, query, persona, date_of_loss, product, "wording", 4))[:3]
    if not wording:
        return {"status": "refused", "pack": None, "reason": "No policy wording found for this condition."}

    # riders: skip the 'scope' clause, keep the rest in clause order (so the benefit clause is included)
    riders = [r for r in keep(_fetch(vec, query, persona, date_of_loss, product, "rider", 5))
              if not r["citation"].endswith("§1")]
    riders = sorted(riders, key=lambda r: _num(r["citation"]))[:3]

    # SOPs: use the SOP written for this condition if there is one, otherwise the best general matches
    sops_all = keep(_fetch(vec, query, persona, date_of_loss, product, "sop", 8))
    pref = CONDITION_SOP.get(condition)
    sops = [r for r in sops_all if pref and r["doc_id"] == pref]
    sops = sorted(sops, key=lambda r: _num(r["citation"]))[:4] if sops else sops_all[:3]

    ver = next(p for p in tools._PRODUCTS if p["product"] == product and p["version"] == calc["version"])
    doc = ver["wording_doc_id"]
    cites = {r["citation"] for r in wording + riders + sops}

    L = [f"# Evidence pack: {condition.replace('_', ' ')} | {product} (version {calc['version']})",
         f"Role: {persona} | Policy start: {policy_start} | Date of loss: {date_of_loss}", "",
         "## 1. Relevant clauses"]
    L += [f"- {r['citation']} ({r['heading']}): {_excerpt(r['content'], terms)} [{r['citation']}]" for r in wording]

    L += ["", "## 2. Calculations (computed by code, not by the model)"]
    if not calc["covered"]:
        L.append(f"- Under {calc['version']} the wording states this condition is excluded [{calc['citation']}]")
        cites.add(calc["citation"])
    else:
        where = "inside" if calc["within_waiting_period"] else "outside"
        L += [f"- Policy version in force on the date of loss: {calc['version']} (wording {doc}) [{calc['citation']}]",
              f"- Waiting period: {calc['waiting_months']} months from the policy start date [{calc['citation']}]",
              f"- Eligible from: {calc['eligible_from']} [{calc['citation']}]",
              f"- The date of loss {date_of_loss} falls {where} the waiting period [{calc['citation']}]"]
        cites.add(calc["citation"])
    lim = next((l for l in tools._LIMITS if l["product"] == product and l["version"] == calc["version"]
                and l["item"] == condition), None)
    if lim:
        c = f"{doc}§{lim['clause_ref']}"; cites.add(c)
        L.append(f"- Sub-limit: {inr(lim['limit_inr'])} ({lim['basis'].replace('_', ' ')}) [{c}]")
    c = f"{doc}§8.1"; cites.add(c)
    L.append(f"- Room rent limit: {ver['room_rent_pct_of_si']}% of sum insured per day [{c}]")

    L += ["", "## 3. Exceptions to check"]
    L += [f"- {r['citation']} ({r['heading']}): {_excerpt(r['content'], terms, 220)} [{r['citation']}]" for r in riders]
    c = f"{doc}§9.2"; cites.add(c)
    L.append(f"- Check portability credit for waiting periods already served under prior continuous cover [{c}]")
    L.append("Also confirm in the Policy Schedule which riders are attached.")

    L += ["", "## 4. SOP steps"]
    L += ([f"- {r['citation']} ({r['heading']}): {_excerpt(r['content'], terms, 220)} [{r['citation']}]" for r in sops]
          or ["- No matching SOP found. Ask your team lead."])

    L += ["", "## 5. Citations"] + [f"- [{c}]" for c in sorted(cites)]
    L += ["", "This pack describes the rules. The claim decision is made by the human adjuster."]

    pack = "\n".join(L)
    return {"status": "ok", "pack": pack, "citations": sorted(cites),
            "problems": guard.check(pack, cites, wording=False)
                        + guard.check(pack.split("## 3.")[0].split("## 2.")[1], cites),
            "tokens": emb.usage.total_tokens, "cost_usd": round(emb.usage.total_tokens / 1e6 * 0.02, 8)}