from src.agentic_rag.chunking import load_chunks


def main():
    chunks = load_chunks()

    print("Q4 - Chunking")
    print(f"Number of chunks: {len(chunks)}")

    print("\nFirst chunk:")
    print(f"Filename: {chunks[0]['filename']}")
    print(f"Content preview:\n{chunks[0]['content'][:500]}")


if __name__ == "__main__":
    main()
