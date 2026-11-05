import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()
client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
)

# 1. Chat test
r = client.chat.completions.create(
    model=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"],
    messages=[{"role": "user", "content": "Reply with exactly: ClaimsIQ chat OK"}],
    temperature=0,
)
print(r.choices[0].message.content)
print("tokens in/out:", r.usage.prompt_tokens, r.usage.completion_tokens)

# 2. Embedding test
e = client.embeddings.create(
    model=os.environ["AZURE_OPENAI_EMBED_DEPLOYMENT"],
    input="Joint replacement surgery waiting period",
)
print("embedding dimensions:", len(e.data[0].embedding))   # must be 1536   