from minsearch import Index

from src.agentic_rag.data_loader import load_documents
from src.agentic_rag.chunking import load_chunks


def build_index():
    documents = load_documents()

    index = Index(
        text_fields=["content"],
        keyword_fields=["filename"],
    )

    index.fit(documents)

    return index


def build_chunk_index():
    chunks = load_chunks()

    index = Index(
        text_fields=["content"],
        keyword_fields=["filename"],
    )

    index.fit(chunks)

    return index