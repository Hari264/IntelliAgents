import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex, SearchField, SearchFieldDataType, SimpleField, SearchableField,
    VectorSearch, HnswAlgorithmConfiguration, VectorSearchProfile,
    SemanticConfiguration, SemanticPrioritizedFields, SemanticField, SemanticSearch)

load_dotenv(override=True)
client = SearchIndexClient(os.environ["AZURE_SEARCH_ENDPOINT"],
                           AzureKeyCredential(os.environ["AZURE_SEARCH_API_KEY"]))
INDEX = os.environ["AZURE_SEARCH_INDEX"]

S = SearchFieldDataType
fields = [
    SimpleField(name="id",             type=S.String, key=True, filterable=True),
    SimpleField(name="doc_id",         type=S.String, filterable=True, facetable=True),
    SearchableField(name="title",      type=S.String),
    SimpleField(name="citation",       type=S.String, filterable=True),
    SimpleField(name="clause_number",  type=S.String, filterable=True),
    SearchableField(name="heading_title", type=S.String),
    SearchableField(name="content",    type=S.String),
    # ---- filter fields (version-correct + role-aware) ----
    SimpleField(name="product",        type=S.String, filterable=True, facetable=True),
    SimpleField(name="version",        type=S.String, filterable=True, facetable=True),
    SimpleField(name="doc_type",       type=S.String, filterable=True, facetable=True),
    SimpleField(name="sensitivity",    type=S.String, filterable=True, facetable=True),
    SimpleField(name="audience",       type=S.Collection(S.String), filterable=True, facetable=True),
    SimpleField(name="effective_from", type=S.DateTimeOffset, filterable=True, sortable=True),
    SimpleField(name="effective_to",   type=S.DateTimeOffset, filterable=True, sortable=True),
    SimpleField(name="word_count",     type=S.Int32, filterable=True),
    # ---- vector field: 1,536 numbers from text-embedding-3-small ----
    SearchField(name="content_vector", type=S.Collection(S.Single), searchable=True, hidden=True,
                vector_search_dimensions=1536, vector_search_profile_name="vec-profile"),
    SimpleField(name="embedding_model", type=S.String),
    SimpleField(name="chunk_hash",      type=S.String),
]

vector_search = VectorSearch(
    algorithms=[HnswAlgorithmConfiguration(name="hnsw-cosine",
                                           parameters={"metric": "cosine"})],
    profiles=[VectorSearchProfile(name="vec-profile", algorithm_configuration_name="hnsw-cosine")],
)

semantic = SemanticSearch(
    default_configuration_name="sem-config",
    configurations=[SemanticConfiguration(
        name="sem-config",
        prioritized_fields=SemanticPrioritizedFields(
            title_field=SemanticField(field_name="title"),
            content_fields=[SemanticField(field_name="content")],
            keywords_fields=[SemanticField(field_name="heading_title")],
        ))],
)

index = SearchIndex(name=INDEX, fields=fields, vector_search=vector_search, semantic_search=semantic)

if INDEX in list(client.list_index_names()):
    print("index exists - deleting and recreating")
    client.delete_index(INDEX)

client.create_index(index)
created = client.get_index(INDEX)
print(f"created index '{created.name}' with {len(created.fields)} fields")
print("vector field dims:", next(f.vector_search_dimensions for f in created.fields if f.name == "content_vector"))
print("semantic config  :", created.semantic_search.default_configuration_name)