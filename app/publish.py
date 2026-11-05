import re, hashlib, yaml
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from app.config import aoai, EMBED_MODEL, CHAT_MODEL
import os
from app import refusals

# Writing to the index needs the ADMIN key (the agent itself uses a read-only query key)
_admin = SearchClient(os.environ["AZURE_SEARCH_ENDPOINT"], os.environ["AZURE_SEARCH_INDEX"],
                      AzureKeyCredential(os.environ["AZURE_SEARCH_API_KEY"]))

FRONT = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.S)
HEAD = re.compile(r"^## (Section) (\d+)\s+(.+)$", re.M)

def publish(rid):
    item = refusals.get_refusal(rid)
    if not item or item["status"] != "approved":
        raise ValueError(f"refusal {rid} must be 'approved' before it can be indexed "
                         f"(it is {item['status'] if item else 'missing'}).")
    m = FRONT.match(item["draft"])
    meta, body = yaml.safe_load(m.group(1)), m.group(2)

    found = list(HEAD.finditer(body))
    chunks = []
    for i, h in enumerate(found):
        end = found[i + 1].start() if i + 1 < len(found) else len(body)
        chunks.append((h.group(2), h.group(3).strip(), body[h.start():end].strip()))

    texts = [f"{meta['title']} | product: {meta['product']} | version: {meta['version']}\n{c[2]}" for c in chunks]
    vecs = [d.embedding for d in aoai.embeddings.create(model=EMBED_MODEL, input=texts).data]

    docs = []
    for (num, heading, content), vec in zip(chunks, vecs):
        docs.append({
            "id": f"{meta['doc_id']}__{num}", "doc_id": meta["doc_id"], "title": meta["title"],
            "citation": f"{meta['doc_id']}§{num}", "clause_number": num, "heading_title": heading,
            "content": content, "product": meta["product"], "version": str(meta["version"]),
            "doc_type": meta["doc_type"], "sensitivity": meta["sensitivity"],
            "audience": list(meta["audience"]),
            "effective_from": f"{str(meta['effective_from'])[:10]}T00:00:00Z",
            "effective_to": f"{str(meta['effective_to'])[:10]}T00:00:00Z",
            "word_count": len(content.split()), "content_vector": vec,
            "embedding_model": EMBED_MODEL,
            "chunk_hash": hashlib.sha256(content.encode("utf-8")).hexdigest()})

    results = _admin.upload_documents(documents=docs)
    failed = [(r.key, r.error_message) for r in results if not r.succeeded]
    if failed:
        raise RuntimeError(f"upload failed: {failed}")
    refusals.mark_indexed(rid)
    return {"doc_id": meta["doc_id"], "chunks": len(docs), "citations": [d["citation"] for d in docs]}

def unpublish(doc_id):
    """Remove a published document from the index (used to reset the demo)."""
    hits = list(_admin.search("*", filter=f"doc_id eq '{doc_id}'", select=["id"]))
    if hits:
        _admin.delete_documents(documents=[{"id": h["id"]} for h in hits])
    return len(hits)