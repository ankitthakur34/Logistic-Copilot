# scripts/test_parent_metadata.py

from app.rag.loader.json_loader import JsonLoader
from app.rag.chunking.parent_child_chunker import ParentChildChunker

loader = JsonLoader("data/json")

docs = loader.load()

chunker = ParentChildChunker()

result = chunker.chunk_documents(docs)
print(result)

for p in result.data:

    if (
        p.metadata.get("shipment_id") == "SHP0102"
        or p.metadata.get("shipment") == "SHP0102"
    ):

        print(p.id)
        print(p.metadata)