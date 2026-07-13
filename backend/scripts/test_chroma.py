from app.rag.vector_store.chroma_vector_store import (
    ChromaVectorStore,
)

vs = ChromaVectorStore()

collection = vs.collection



res = collection.get(
    where={
        "shipment_id:": "SHP0102"
    }
)
print(res)
print(res["ids"])
print(res["metadatas"])