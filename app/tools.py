import re
import csv
from datetime import date
from dateutil.relativedelta import relativedelta
from azure.search.documents.models import VectorizedQuery
from app.config import aoai, search, EMBED_MODEL, PERSONAS, PRODUCTS, ROOT

# ---------------- strict key-term matching (synonyms + generic words ignored) ----------------
_STOP = {"the", "and", "for", "with", "under", "ion"}

# Generic words that say nothing about the subject. They never count as "missing".
_GENERIC = {"cover", "covers", "covered", "coverage", "policy", "policies", "claim", "claims",
            "benefit", "benefits", "eligible", "eligibility", "apply", "applies", "applicable",
            "loss", "date", "fall", "falls", "inside", "rule", "rules", "limit", "information",
            "details", "customer", "treatment"}

# Words the user may type -> words the documents actually use
_ALIASES = {
    "knee":         ["joint replacement", "arthroplasty"],
    "hip":          ["joint replacement", "arthroplasty"],
    "joint":        ["joint replacement", "arthroplasty"],
    "ped":          ["pre-existing"],
    "pre existing": ["pre-existing"],
    "delivery":     ["maternity"],
    "pregnancy":    ["maternity"],
    "eye":          ["cataract"],
    "dental":       ["dental", "teeth"],
}

def _words_in(term, text):
    """True if every significant (non-generic) word of the term appears at a word start in the text."""
    words = [w for w in re.findall(r"[a-z0-9]+", term.lower())
             if len(w) > 2 and w not in _STOP and w not in _GENERIC]
    return all(re.search(rf"\b{re.escape(w)}", text) for w in words) if words else True

def _term_in(term, text):
    """True if the term, or a known synonym of it, appears in the evidence text."""
    t = term.lower().strip()
    if _words_in(t, text):
        return True
    return any(_words_in(alt, text)
               for key, alts in _ALIASES.items()
               if re.search(rf"\b{re.escape(key)}\b", t)
               for alt in alts)

# ---------------- search tool ----------------
def _search(query, vec, flt, top):
    res = search.search(
        search_text=query,
        vector_queries=[VectorizedQuery(vector=vec, k_nearest_neighbors=20, fields="content_vector")],
        filter=flt, query_type="semantic", semantic_configuration_name="sem-config", top=top,
        select=["citation", "doc_id", "version", "doc_type", "heading_title", "content"])
    return [{"citation": r["citation"], "doc_id": r["doc_id"], "version": r["version"],
             "doc_type": r["doc_type"], "heading": r["heading_title"],
             "rerank": round(r["@search.reranker_score"] or 0, 2), "content": r["content"]}
            for r in res]

def search_clauses(query, persona, date_of_loss=None, key_terms=None, product="HEALTH_GOLD", top=5):
    """Hybrid search filtered by date of loss and role. Returns evidence + a coverage flag."""
    if persona not in PERSONAS:
        raise ValueError(f"unknown persona {persona!r}")
    if product not in PRODUCTS:
        raise ValueError(f"unknown product {product!r}")
    d = date.fromisoformat(date_of_loss).isoformat() if date_of_loss else date.today().isoformat()

    aud = " or ".join(f"a eq '{a}'" for a in PERSONAS[persona])
    base = (f"product eq '{product}' and effective_from le {d}T00:00:00Z "
            f"and effective_to ge {d}T00:00:00Z and audience/any(a: {aud})")

    vec = aoai.embeddings.create(model=EMBED_MODEL, input=query).data[0].embedding
    wording = _search(query, vec, base + " and doc_type eq 'wording'", top=2)   # authoritative clauses first
    general = _search(query, vec, base, top=top)

    evidence, seen = [], set()
    for r in wording + general:
        if r["citation"] not in seen:
            seen.add(r["citation"]); evidence.append(r)

    text = " ".join(r["content"].lower() for r in evidence)
    terms = [t.strip().lower() for t in (key_terms or []) if t.strip()]
    missing = [t for t in terms if not _term_in(t, text)]
    covered = not missing                      # every meaningful key term (or its synonym) must appear
    return {"date_used": d, "persona": persona, "covered": covered,
            "missing_terms": missing, "evidence": evidence}

# ---------------- exact tools (no model guessing) ----------------
def _read_csv(name):
    with open(ROOT / "data" / "reference" / f"{name}.csv", encoding="utf-8-sig") as f:
        return [{k.strip(): (v or "").strip() for k, v in row.items()} for row in csv.DictReader(f)]

_CODES    = {r["code"].upper(): r for r in _read_csv("rejection_codes")}
_WAITING  = _read_csv("waiting_periods")
_PRODUCTS = _read_csv("products")
_LIMITS   = _read_csv("sub_limits")

def lookup_rejection_code(code):
    """Exact lookup of a rejection code. Returns reason, clause, script id and next action."""
    row = _CODES.get(str(code).strip().upper())
    if not row:
        return {"found": False, "code": code, "message": "Rejection code not found in the catalogue."}
    return {"found": True, **row}

def _version_for(product, d):
    for p in _PRODUCTS:
        if p["product"] == product and p["effective_from"] <= d <= p["effective_to"]:
            return p
    return None

def compute_waiting_period(condition, policy_start, date_of_loss, product="HEALTH_GOLD"):
    """Which policy version applies, the waiting months for it, the eligible date, and whether the loss falls inside it."""
    try:
        start = date.fromisoformat(policy_start)
        loss = date.fromisoformat(date_of_loss)
    except ValueError:
        return {"ok": False, "message": "Dates must be YYYY-MM-DD."}

    ver = _version_for(product, loss.isoformat())
    if not ver:
        return {"ok": False, "message": f"No {product} version is in force on {loss}."}

    row = next((w for w in _WAITING if w["product"] == product and w["version"] == ver["version"]
                and w["condition"] == condition), None)
    if not row:
        return {"ok": False, "message": f"No waiting period recorded for '{condition}'.",
                "known_conditions": sorted({w["condition"] for w in _WAITING if w["product"] == product})}
    if row["covered"].lower() != "true":
        return {"ok": True, "covered": False, "version": ver["version"], "condition": condition,
                "citation": f"{ver['wording_doc_id']}§{row['clause_ref']}",
                "message": "This condition is not covered under this policy version."}

    months = int(row["waiting_months"])
    eligible = start + relativedelta(months=months)
    return {"ok": True, "covered": True, "product": product, "version": ver["version"],
            "condition": condition, "waiting_months": months, "policy_start": str(start),
            "date_of_loss": str(loss), "eligible_from": str(eligible),
            "within_waiting_period": loss < eligible,
            "citation": f"{ver['wording_doc_id']}§{row['clause_ref']}"}