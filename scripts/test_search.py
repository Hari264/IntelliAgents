import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient

load_dotenv(override=True)
endpoint = os.environ["AZURE_SEARCH_ENDPOINT"]
print("endpoint:", endpoint)

client = SearchIndexClient(endpoint, AzureKeyCredential(os.environ["AZURE_SEARCH_API_KEY"]))
print("existing indexes:", list(client.list_index_names()))   # [] is expected for a new service
print("Search connection: OK")