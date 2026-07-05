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

query_embedding = embedding_model.embed_query(
    query
)

retriever = ChromaRetriever(
    vector_store=ChromaVectorStore(),
)

result = retriever.retrieve(
    query_embedding=query_embedding,
    top_k=5,
)

print("=" * 80)
print("Retrieved")
print("=" * 80)

for i in range(len(result.ids)):

    print()

    print("Rank :", i + 1)

    print("ID :", result.ids[i])

    print("Score :", result.scores[i])

    print("Metadata :", result.metadatas[i])

    print()

    print(result.documents[i][:300])

    print("-" * 80)