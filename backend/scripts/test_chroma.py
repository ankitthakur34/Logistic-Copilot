from app.rag.vector_store.chroma_vector_store import (
    ChromaVectorStore,
)

vs = ChromaVectorStore()

collection = vs.collection

print()
print("=" * 100)
print("TOTAL")
print("=" * 100)

print(collection.count())

print()
print("=" * 100)
print("SAMPLE METADATA")
print("=" * 100)

data = collection.get(
    limit=20,
    include=["metadatas"]
)

for m in data["metadatas"]:

    print(m)
    print("-" * 80)