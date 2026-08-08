from src.agentic_rag.search import build_index


QUERY = "How does the agentic loop keep calling the model until it stops?"


index = build_index()

results = index.search(
    QUERY,
    boost_dict={},
    num_results=5,
)

print("Q2 - Search Query:")
print(QUERY)

print("\nSearch Results:")

for result in results:
    print(f"- {result['filename']}")