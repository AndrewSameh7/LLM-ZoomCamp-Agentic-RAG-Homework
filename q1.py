from src.agentic_rag.data_loader import load_documents


documents = load_documents()

print(f"Number of documents: {len(documents)}")

print("\nFirst document:")
print(f"Filename: {documents[0]['filename']}")
print(f"Content preview:\n{documents[0]['content'][:500]}")