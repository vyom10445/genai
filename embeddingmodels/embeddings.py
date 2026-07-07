from dotenv import load_dotenv
load_dotenv()

from langchain_openai import OpenAIEmbeddings

embedding = OpenAIEmbeddings(
    model="text-embedding-3-small",
    dimensions=64
    )

text = [
    "my name is vyom",
    "what's up!",
    "im learning genai"
]

vector = embedding.embed_documents(text)

print(vector)