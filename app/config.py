import os, csv
from pathlib import Path
from dotenv import load_dotenv
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env", override=True)

CHAT_MODEL  = os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"]
EMBED_MODEL = os.environ["AZURE_OPENAI_EMBED_DEPLOYMENT"]

aoai = AzureOpenAI(azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
                   api_key=os.environ["AZURE_OPENAI_API_KEY"],
                   api_version=os.environ["AZURE_OPENAI_API_VERSION"])

# Use the read-only query key if you made one, otherwise fall back to the admin key
_search_key = os.environ.get("AZURE_SEARCH_QUERY_KEY") or os.environ["AZURE_SEARCH_API_KEY"]
search = SearchClient(os.environ["AZURE_SEARCH_ENDPOINT"], os.environ["AZURE_SEARCH_INDEX"],
                      AzureKeyCredential(_search_key))

def load_personas():
    """persona -> list of audiences it may see. One source of truth: personas.csv"""
    with open(ROOT / "data" / "reference" / "personas.csv", encoding="utf-8-sig") as f:
        return {r["persona"].strip(): r["allowed_audience"].strip().split("|")
                for r in csv.DictReader(f)}

PERSONAS = load_personas()
PRODUCTS = {"HEALTH_GOLD", "HEALTH_SILVER"}