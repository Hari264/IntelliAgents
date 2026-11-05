import re

REFUSAL = "REFUSE: insufficient evidence"
RESTRICTED_MSG = "BLOCKED: this content is restricted for your role."

# Doc id + clause, e.g. HG-WORD-2025§4.2 or SCR-PED-01§2
CITE = re.compile(r"\b([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+)§(\d+(?:\.\d+)*)")

DECISION_PATTERNS = [
    r"\b(is|are|was|has been|have been|will be|be|been)\s+(not\s+)?(approved|rejected|denied|declined|accepted)\b",
    r"\bnot payable\b",
    r"\bis\s+(not\s+)?payable\b",
    r"\b(we|i)\s+(will|shall|can|must)\s+(approve|reject|deny|decline|pay)\b",
    r"\bclaim\s+(should|must)\s+be\s+(paid|settled|approved|rejected|denied)\b",
    r"\b(claim|it)\b[^.\n]{0,60}\bis not covered\b",
]

RESTRICTED_TOPICS = [
    r"\bsiu\b",
    r"red[\s-]?flag",
    r"watch\s?list",
    r"fraud[^.?]*\b(threshold|trigger|score|amount|limit|rule)s?\b",
    r"\b(threshold|trigger)s?\b[^.?]*fraud",
]

def is_restricted(question, persona_audiences):
    """Fraud-playbook topics are blocked for any role that has no 'fraud' audience."""
    if "fraud" in persona_audiences:
        return False
    return any(re.search(p, question, re.I) for p in RESTRICTED_TOPICS)

def normalise(answer, allowed):
    """Rewrite sub-clause citations (HG-WORD-2025§4.2.1) to the clause that was actually retrieved (HG-WORD-2025§4.2)."""
    def fix(m):
        doc, parts = m.group(1), m.group(2).split(".")
        while parts:
            cand = f"{doc}§{'.'.join(parts)}"
            if cand in allowed:
                return cand
            parts.pop()
        return m.group(0)                 # left as is -> check() will flag it
    return CITE.sub(fix, answer)

def check(answer, allowed, wording=True):
    """Return a list of problems. An empty list means the answer passes.
    wording=False skips the decision-word check (use it for text that quotes the policy)."""
    problems = []
    codes = [a for a in allowed if a.startswith("CL-")]

    bad = sorted({f"{d}§{n}" for d, n in CITE.findall(answer) if f"{d}§{n}" not in allowed})
    if bad:
        problems.append("These citations were not in the retrieved evidence: " + ", ".join(bad))

    if not CITE.search(answer) and not any(c in answer for c in codes):
        problems.append("The answer has no citations.")

    for line in answer.splitlines():
        s = line.strip()
        if s.startswith(("-", "•", "*")) and not (CITE.search(s) or any(c in s for c in codes)):
            problems.append(f"This bullet has no citation: {s[:70]}")

    if wording:
        for p in DECISION_PATTERNS:
            m = re.search(p, answer, re.I)
            if m:
                problems.append(f"Decision wording is not allowed: '{m.group(0)}'. "
                                "Say the date of loss falls inside or outside the waiting period instead.")
    return problems