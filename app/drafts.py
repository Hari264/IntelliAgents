import re, yaml
from app.config import aoai, CHAT_MODEL, ROOT
from app import tools, refusals
from app.agent import PRICE_IN, PRICE_OUT

SYSTEM = """You write DRAFT internal guidance for a health-insurer knowledge base. A subject-matter expert (SME) will review it before use.

RULES
1. Use ONLY the reference clauses provided. Do not invent new percentages, amounts, periods or limits.
2. NEVER assign a class, loading, premium or limit to the subject by analogy or comparison with other listed items. If the reference does not list the subject, the draft must say the subject is not listed and must be referred to the responsible senior person named in the reference (for example the Chief Underwriter). Do not quote any percentage in the draft.
3. Useful content for such a gap: why the subject is not listed, the information the underwriter should collect before referring (for example nature of storage, quantities, fire-safety measures, location), and the rule that no provisional premium or terms are given before the decision.
4. Use the exact subject words from the user's question (for example the hazard or product name) in the headings and in the text, so the guidance can be found later.
5. Write 3 sections. Each heading is exactly: ## Section N Title  (N = 1, 2, 3)
6. Section 1 is Purpose and Scope. Section 3 is Referral and Limits.
7. Each section is 80-200 words of plain prose or numbered sub-points (2.1, 2.2). Each section must make sense on its own.
8. Never say a claim or proposal is approved, rejected or declined.
9. Output ONLY the sections. No title, no introduction, no code fences."""

NUM = re.compile(r"₹[\d,]+|\d+(?:\.\d+)?\s?%|\d+\s*(?:months?|days?|years?)", re.I)

def _norm(s):
    return re.sub(r"\s+", "", s.lower())

def make_draft(rid):
    item = refusals.get_refusal(rid)
    if not item:
        raise ValueError(f"refusal {rid} not found")
    if item["status"] not in ("open", "drafted"):
        raise ValueError(f"refusal {rid} is {item['status']}, not open")

    # Reference: what this role can already see on the subject (role + date filters apply)
    ev = tools.search_clauses(item["question"], item["persona"], item["date_of_loss"] or None)["evidence"][:4]
    context = "\n\n".join(f"[{e['citation']}]\n{e['content']}" for e in ev)

    resp = aoai.chat.completions.create(
        model=CHAT_MODEL, temperature=0,
        messages=[{"role": "system", "content": SYSTEM},
                  {"role": "user", "content":
                   f"Question that could not be answered:\n{item['question']}\n\n"
                   f"Key terms: {item['key_terms']}\n\nReference clauses:\n{context}"}])
    body = (resp.choices[0].message.content or "").strip()
    body = re.sub(r"^```[a-z]*\n|\n```$", "", body).strip()

    heads = re.findall(r"^## Section (\d+) (.+)$", body, re.M)
    problems = []
    if not body.startswith("## Section 1 "):
        problems.append("draft does not start with '## Section 1'")
    if not 3 <= len(heads) <= 5:
        problems.append(f"draft has {len(heads)} sections, expected 3-5")
    if "%" in body:
        problems.append("draft contains a percentage; the SME must confirm it is not assigned by analogy")
    if "chief underwriter" in context.lower() and "chief underwriter" not in body.lower():
        problems.append("draft does not tell the reader to refer to the Chief Underwriter")
    if re.search(r"consistent with class|falls? (under|into) class|attract", body, re.I):
        problems.append("draft appears to assign a class by analogy")

    allowed = _norm(context + " " + item["question"])
    new_numbers = sorted({n.strip() for n in NUM.findall(body) if _norm(n) not in allowed})

    doc_id = f"APPR-{rid:03d}"
    title = ("Proposed guidance for: " + item["question"][:80]).replace('"', "'")
    header = (f'---\ndoc_id: {doc_id}\ntitle: "{title}"\nproduct: HEALTH_GOLD\nversion: na\n'
              f'effective_from: 2024-01-01\neffective_to: 9999-12-31\ndoc_type: approved_guidance\n'
              f'audience: [{item["persona"]}]\nsensitivity: Internal\n---\n')
    markdown = header + body + "\n"
    yaml.safe_load(markdown.split("---")[1])          # header must parse

    refusals.save_draft(rid, doc_id, markdown)
    out = ROOT / "logs" / "drafts"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{doc_id}.md").write_text(markdown, encoding="utf-8")

    cost = resp.usage.prompt_tokens / 1e6 * PRICE_IN + resp.usage.completion_tokens / 1e6 * PRICE_OUT
    return {"doc_id": doc_id, "markdown": markdown, "sections": len(heads), "problems": problems,
            "new_numbers": new_numbers, "reference": [e["citation"] for e in ev], "cost_usd": round(cost, 5)}