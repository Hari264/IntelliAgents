import os
from datetime import date
from azure.search.documents.models import VectorizedQuery
from test_hybrid import aoai, search, PERSONA_AUDIENCE   # reuses the clients from the last script

def search_v2(query, persona, date_of_loss=None, product="HEALTH_GOLD", top=5, doc_type=None):
    d = date_of_loss or date.today().isoformat()
    aud = " or ".join(f"a eq '{a}'" for a in PERSONA_AUDIENCE[persona])
    flt = (f"product eq '{product}' and effective_from le {d}T00:00:00Z "
           f"and effective_to ge {d}T00:00:00Z and audience/any(a: {aud})")
    if doc_type:
        flt += f" and doc_type eq '{doc_type}'"
    vec = aoai.embeddings.create(model=os.environ["AZURE_OPENAI_EMBED_DEPLOYMENT"],
                                 input=query).data[0].embedding
    res = search.search(search_text=query,
        vector_queries=[VectorizedQuery(vector=vec, k_nearest_neighbors=20, fields="content_vector")],
        filter=flt, query_type="semantic", semantic_configuration_name="sem-config",
        top=top, select=["citation", "version", "doc_type", "content"])
    return [{"citation": r["citation"], "version": r["version"], "doc_type": r["doc_type"],
             "rerank": round(r["@search.reranker_score"] or 0, 2), "content": r["content"]} for r in res]

def retrieve(query, persona, date_of_loss=None, key_terms=()):
    primary = search_v2(query, persona, date_of_loss, top=2, doc_type="wording")   # authoritative clauses
    general = search_v2(query, persona, date_of_loss, top=5)
    merged, seen = [], set()
    for r in primary + general:
        if r["citation"] not in seen:
            seen.add(r["citation"]); merged.append(r)
    text = " ".join(r["content"].lower() for r in merged)
    covered = (not key_terms) or any(t.lower() in text for t in key_terms)
    return merged, covered

def show(title, rows, covered):
    print(f"\n=== {title}   | key terms found in evidence: {covered}")
    for r in rows:
        print(f"  {r['citation']:<22}{r['version']:<6}{r['doc_type']:<14} rerank={r['rerank']}")

q = "Is knee replacement covered and what is the waiting period?"
rows, cov = retrieve(q, "adjuster", "2024-09-15", key_terms=["joint replacement"])
show("1. Knee, loss 2024-09-15", rows, cov)
rows, cov = retrieve(q, "adjuster", "2025-09-15", key_terms=["joint replacement"])
show("2. Knee, loss 2025-09-15", rows, cov)
rows, cov = retrieve("What occupational loading applies to staff at a lithium-ion battery storage warehouse?",
                     "underwriter", key_terms=["lithium", "battery"])
show("3. Li-ion warehouse (should be NOT covered -> refuse)", rows, cov)
rows, cov = retrieve("What is the international emergency evacuation benefit limit?",
                     "adjuster", "2025-06-01", key_terms=["international", "evacuation"])
show("4. International evacuation (should be NOT covered -> refuse)", rows, cov)