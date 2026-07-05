from app.rag.embeddings.sentence_transformer_embedding import (
    SentenceTransformerEmbedding,
)

from app.rag.vector_store.chroma_vector_store import (
    ChromaVectorStore,
)

from app.rag.retrieval.chroma_retriever import (
    ChromaRetriever,
)

embedding_model = SentenceTransformerEmbedding()

query = "Why is shipment SHP0007 delayed?"

print("=" * 70)
print("QUESTION")
print("=" * 70)

print(query)

print()

print("=" * 70)
print("EMBED QUERY")
print("=" * 70)

query_embedding = embedding_model.embed_query(
    query
)

print(
    "Embedding Dimension:",
    len(query_embedding),
)

print()

print("=" * 70)
print("SEARCH")
print("=" * 70)

retriever = ChromaRetriever(
    vector_store=ChromaVectorStore(),
)

result = retriever.retrieve(
    query_embedding=query_embedding,
    top_k=5,
)

print()

for rank in range(len(result.ids)):

    print("=" * 70)

    print(f"Rank : {rank + 1}")

    print(f"ID : {result.ids[rank]}")

    print(f"Score : {result.scores[rank]}")

    print(f"Metadata : {result.metadatas[rank]}")

    print()

    print(result.documents[rank])

    print()