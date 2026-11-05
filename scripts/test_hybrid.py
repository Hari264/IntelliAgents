import os
from datetime import date
from dotenv import load_dotenv
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery

load_dotenv(override=True)
aoai = AzureOpenAI(azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
                   api_key=os.environ["AZURE_OPENAI_API_KEY"],
                   api_version=os.environ["AZURE_OPENAI_API_VERSION"])
search = SearchClient(os.environ["AZURE_SEARCH_ENDPOINT"], os.environ["AZURE_SEARCH_INDEX"],
                      AzureKeyCredential(os.environ["AZURE_SEARCH_API_KEY"]))

PERSONA_AUDIENCE = {"service": ["service"],
                    "adjuster": ["adjuster", "fraud"],
                    "underwriter": ["underwriter"]}

def search_clauses(query, persona, date_of_loss=None, product="HEALTH_GOLD", top=5):
    d = date_of_loss or date.today().isoformat()           # no date given -> today
    aud = " or ".join(f"a eq '{a}'" for a in PERSONA_AUDIENCE[persona])
    flt = (f"product eq '{product}' "
           f"and effective_from le {d}T00:00:00Z and effective_to ge {d}T00:00:00Z "
           f"and audience/any(a: {aud})")
    vec = aoai.embeddings.create(model=os.environ["AZURE_OPENAI_EMBED_DEPLOYMENT"],
                                 input=query).data[0].embedding
    results = search.search(
        search_text=query,
        vector_queries=[VectorizedQuery(vector=vec, k_nearest_neighbors=20, fields="content_vector")],
        filter=flt,
        query_type="semantic", semantic_configuration_name="sem-config",
        top=top, select=["citation", "version", "doc_type", "heading_title"])
    return [{"citation": r["citation"], "version": r["version"], "doc_type": r["doc_type"],
             "score": round(r["@search.score"], 3),
             "rerank": round(r["@search.reranker_score"] or 0, 2)} for r in results]

def show(title, rows):
    print(f"\n=== {title}")
    for r in rows:
        print(f"  {r['citation']:<22}{r['version']:<6}{r['doc_type']:<14} rerank={r['rerank']}")
    if not rows:
        print("  (no results)")

if __name__ == "__main__":
    show("1. Knee replacement, loss 2024-09-15, adjuster",
         search_clauses("Is knee replacement covered and what is the waiting period?", "adjuster", "2024-09-15"))
    show("2. Same question, loss 2025-09-15, adjuster",
         search_clauses("Is knee replacement covered and what is the waiting period?", "adjuster", "2025-09-15"))
    show("3. Meaning match: 'knee surgery' vs 'arthroplasty', 2025",
         search_clauses("how long before knee surgery is covered", "adjuster", "2025-09-15"))
    show("4. Fraud thresholds, SERVICE role (must show no fraud_playbook)",
         search_clauses("What claim amount triggers mandatory SIU referral?", "service", "2025-09-15"))
    show("5. Same question, ADJUSTER role (FRD-01 should be first)",
         search_clauses("What claim amount triggers mandatory SIU referral?", "adjuster", "2025-09-15"))
    show("6. Li-ion warehouse, underwriter (nothing should match well)",
         search_clauses("What occupational loading applies to staff at a lithium-ion battery storage warehouse?", "underwriter"))