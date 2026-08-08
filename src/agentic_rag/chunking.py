from gitsource import chunk_documents

from src.agentic_rag.data_loader import load_documents


def load_chunks():
    documents = load_documents()

    chunks = chunk_documents(
        documents,
        size=2000,
        step=1000,
    )

    return chunks