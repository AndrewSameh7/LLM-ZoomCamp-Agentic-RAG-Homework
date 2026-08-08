import os

from dotenv import load_dotenv
from groq import Groq

from src.agentic_rag.rag import RAGBase
from src.agentic_rag.search import build_chunk_index


QUERY = "How does the agentic loop keep calling the model until it stops?"


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY was not found in .env")


client = Groq(api_key=api_key)

index = build_chunk_index()

rag = RAGBase(
    index=index,
    llm_client=client,
)

answer, usage = rag.rag(QUERY)

print("Q5 - Query:")
print(QUERY)

print("\nAnswer:")
print(answer)

print("\nInput tokens:")
print(usage.prompt_tokens)