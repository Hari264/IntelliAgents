"""Checks all corpus .md files against the hackathon rules. Reports problems instead of crashing."""
import glob, re, yaml

DOCS = "data/docs"     # <-- change this if Step 1 showed a different folder

ALLOWED_TYPES = {"wording","sop","circular","uw_guideline","fraud_playbook",
                 "script","faq","rider","memo","approved_guidance"}
SENS     = {"General","Internal","Restricted"}
AUD      = {"adjuster","service","underwriter","fraud"}
PRODUCTS = {"HEALTH_GOLD","HEALTH_SILVER"}
BANNED   = ["lithium","li-ion","battery","batteries","overseas","international","abroad","evacuation"]
FRAUD_TERMS = ["90 days","90-day","150%","red-flag score","watchlist"]
REQUIRED = ["doc_id","title","product","version","effective_from","effective_to",
            "doc_type","audience","sensitivity"]

FRONT = re.compile(r"^\ufeff?---\s*\n(.*?)\n---\s*\n(.*)$", re.S)
HEAD  = re.compile(r"^## (.+)$", re.M)

files = sorted(glob.glob(f"{DOCS}/**/*.md", recursive=True))
print(f"Found {len(files)} files in '{DOCS}' (expected 50)")
if not files:
    raise SystemExit("No files found - fix the DOCS path at the top of this script.")

ids, errors = set(), []
for p in files:
    text = open(p, encoding="utf-8").read()
    m = FRONT.match(text)
    if not m:
        errors.append(f"{p}: no YAML header (file must start with ---)"); continue
    try:
        meta = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        errors.append(f"{p}: YAML error - {str(e).splitlines()[0]} (an unquoted ':' in a value?)"); continue
    body = m.group(2)

    for f in REQUIRED:
        if f not in meta: errors.append(f"{p}: missing field '{f}'")
    if meta.get("doc_type") not in ALLOWED_TYPES: errors.append(f"{p}: bad doc_type {meta.get('doc_type')!r}")
    if meta.get("sensitivity") not in SENS:       errors.append(f"{p}: bad sensitivity {meta.get('sensitivity')!r}")
    if meta.get("product") not in PRODUCTS:       errors.append(f"{p}: bad product {meta.get('product')!r}")
    if not set(meta.get("audience") or []) <= AUD: errors.append(f"{p}: bad audience {meta.get('audience')}")
    for d in ("effective_from","effective_to"):
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(meta.get(d, ""))[:10]):
            errors.append(f"{p}: {d} is not YYYY-MM-DD")
    if meta.get("doc_id") in ids: errors.append(f"{p}: duplicate doc_id {meta['doc_id']}")
    ids.add(meta.get("doc_id"))

    low = body.lower()
    if meta.get("doc_type") != "approved_guidance":
        for w in BANNED:
            if w in low: errors.append(f"{p}: banned word '{w}'")
    if meta.get("doc_type") != "fraud_playbook":
        for t in FRAUD_TERMS:
            if t in low: errors.append(f"{p}: fraud term '{t}' outside fraud playbook")

    if not body.lstrip().startswith("## "): errors.append(f"{p}: text before the first ## heading")
    for h in HEAD.findall(body):
        if not re.match(r"(Clause|Section) \d+(\.\d+)*\.? ", h):
            errors.append(f"{p}: bad heading '## {h}'")

print(f"{len(files)} documents checked, {len(errors)} problems")
for e in errors: print(" -", e)