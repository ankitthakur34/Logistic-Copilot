from collections import defaultdict

from app.rag.vector_store.chroma_vector_store import (
    ChromaVectorStore,
)

store = ChromaVectorStore()

result = store.collection.get(
    include=["metadatas"]
)

catalog = defaultdict(set)

for metadata in result["metadatas"]:

    for key, value in metadata.items():

        if isinstance(value, list):

            for item in value:

                catalog[key].add(item)

    else:

        catalog[key].add(value)


print("=" * 80)
print("METADATA CATALOG")
print("=" * 80)

for key, values in catalog.items():

    print()

    print(key)

    for value in sorted(values):

        print("  ", value)