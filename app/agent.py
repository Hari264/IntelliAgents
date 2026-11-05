import json
from app.config import aoai, CHAT_MODEL, ROOT, PERSONAS
from app import tools, guard

SYSTEM = (ROOT / "app" / "prompts" / "system_v2.md").read_text(encoding="utf-8")

# approximate Global Standard prices per 1M tokens for gpt-4.1-mini (check your Azure price page)
PRICE_IN, PRICE_OUT = 0.40, 1.60
REFUSAL = guard.REFUSAL

# Rejection codes that are about a waiting period -> the condition to calculate
CODE_CONDITION = {"CL-101": "initial_waiting", "CL-205": "joint_replacement",
                  "CL-217": "pre_existing_disease", "CL-415": "maternity"}

TOOL_SPECS = [
    {"type": "function", "function": {
        "name": "search_clauses",
        "description": "Search the policy wordings, SOPs, scripts, circulars and guidelines. Results are already filtered by the date of loss and the user's role.",
        "parameters": {"type": "object", "properties": {
            "query": {"type": "string", "description": "The search question in plain words"},
            "key_terms": {"type": "array", "items": {"type": "string"},
                          "description": "2-3 distinctive subject words from the user's question, in the user's own words (for example 'lithium', 'battery', 'evacuation', 'joint replacement'). Do NOT include generic words such as policy, coverage, claim or waiting period. Every term must be present in the evidence for an answer to be allowed."}},
            "required": ["query", "key_terms"]}}},
    {"type": "function", "function": {
        "name": "lookup_rejection_code",
        "description": "Exact lookup of a rejection code such as CL-217.",
        "parameters": {"type": "object", "properties": {"code": {"type": "string"}}, "required": ["code"]}}},
    {"type": "function", "function": {
        "name": "compute_waiting_period",
        "description": "ALWAYS use for waiting-period or eligibility-date questions. Picks the policy version in force on the date of loss and does the date maths.",
        "parameters": {"type": "object", "properties": {
            "condition": {"type": "string", "enum": ["initial_waiting", "joint_replacement", "cataract", "hernia",
                                                       "bariatric_surgery", "pre_existing_disease", "maternity"]}},
            "required": ["condition"]}}},
]

def _run_tool(name, args, ctx):
    """The app, not the model, controls persona and dates."""
    if name == "search_clauses":
        r = tools.search_clauses(args.get("query", ""), ctx["persona"], ctx.get("date_of_loss"),
                                 key_terms=args.get("key_terms") or [])
        return {"covered": r["covered"], "missing_terms": r["missing_terms"], "date_used": r["date_used"],
                "evidence": [{"citation": e["citation"], "version": e["version"], "doc_type": e["doc_type"],
                              "text": e["content"]} for e in r["evidence"]]}
    if name == "lookup_rejection_code":
        res = tools.lookup_rejection_code(args.get("code", ""))
        cond = CODE_CONDITION.get(str(args.get("code", "")).strip().upper())
        if res.get("found") and cond and ctx.get("policy_start") and ctx.get("date_of_loss"):
            res["waiting_calculation"] = tools.compute_waiting_period(cond, ctx["policy_start"], ctx["date_of_loss"])
        return res
    if name == "compute_waiting_period":
        if not (ctx.get("policy_start") and ctx.get("date_of_loss")):
            return {"ok": False, "message": "Policy start date and date of loss are required. Ask the user for them."}
        return tools.compute_waiting_period(args["condition"], ctx["policy_start"], ctx["date_of_loss"])
    return {"error": f"unknown tool {name}"}

def _pack(answer, status, called, evidence, flags, tin, tout, info):
    cost = tin / 1e6 * PRICE_IN + tout / 1e6 * PRICE_OUT
    return {"answer": answer, "status": status, "tools_called": called,
            "evidence_citations": sorted(evidence), "covered_flags": flags,
            "tokens_in": tin, "tokens_out": tout, "cost_usd": round(cost, 5), "guard": info}

def run(question, persona, date_of_loss=None, policy_start=None, max_rounds=5):
    # 0. Role block: decided by code, before any model call (costs nothing)
    if guard.is_restricted(question, PERSONAS[persona]):
        return _pack(guard.RESTRICTED_MSG, "blocked", [], set(), [], 0, 0, {"repaired": False, "problems": []})

    ctx = {"persona": persona, "date_of_loss": date_of_loss, "policy_start": policy_start}
    context_line = (f"[Context: role={persona}; date_of_loss={date_of_loss or 'not given'}; "
                    f"policy_start={policy_start or 'not given'}]")
    messages = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": f"{context_line}\n{question}"}]
    tin = tout = 0
    called, evidence, covered_flags = [], set(), []
    answer, finished = "", False

    for _ in range(max_rounds):
        resp = aoai.chat.completions.create(model=CHAT_MODEL, messages=messages, tools=TOOL_SPECS,
                                            tool_choice="auto", temperature=0)
        tin += resp.usage.prompt_tokens
        tout += resp.usage.completion_tokens
        msg = resp.choices[0].message
        if not msg.tool_calls:
            answer, finished = msg.content or "", True
            break
        messages.append(msg)
        for tc in msg.tool_calls:
            args = json.loads(tc.function.arguments or "{}")
            result = _run_tool(tc.function.name, args, ctx)
            if tc.function.name == "search_clauses":
                covered_flags.append(result["covered"])
            called.append({"tool": tc.function.name, "args": args})
            for e in result.get("evidence", []):
                evidence.add(e["citation"])
            if result.get("citation"):
                evidence.add(result["citation"])
            if result.get("found"):
                evidence.add(str(result["code"]).upper())
            if result.get("waiting_calculation", {}).get("citation"):
                evidence.add(result["waiting_calculation"]["citation"])
            messages.append({"role": "tool", "tool_call_id": tc.id,
                             "content": json.dumps(result, ensure_ascii=False, default=str)})

    info = {"repaired": False, "problems": []}

    # 1. Refusals decided by code
    if not finished or (covered_flags and not any(covered_flags)) or answer.strip().startswith("REFUSE"):
        return _pack(REFUSAL, "refused", called, evidence, covered_flags, tin, tout, info)

    # 2. Citation and wording checks, with one repair attempt
    answer = guard.normalise(answer, evidence)
    problems = guard.check(answer, evidence)
    if problems:
        info["problems"] = problems
        messages.append({"role": "assistant", "content": answer})
        messages.append({"role": "user", "content":
            "Your answer failed these checks:\n- " + "\n- ".join(problems) +
            "\nRewrite the whole answer and fix them. Use only citations from the tool results, "
            "exactly as [DOC-ID§clause], one per bracket. Keep the same format."})
        resp = aoai.chat.completions.create(model=CHAT_MODEL, messages=messages, tools=TOOL_SPECS,
                                            tool_choice="none", temperature=0)
        tin += resp.usage.prompt_tokens
        tout += resp.usage.completion_tokens
        answer = guard.normalise(resp.choices[0].message.content or "", evidence)
        info["repaired"] = True
        if guard.check(answer, evidence):
            return _pack(REFUSAL, "refused", called, evidence, covered_flags, tin, tout, info)

    return _pack(answer, "answered", called, evidence, covered_flags, tin, tout, info)