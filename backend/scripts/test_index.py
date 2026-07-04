from app.rag.loader.markdown_loader import MarkdownLoader
from app.rag.chunking.parent_child_chunker import ParentChildChunker
from app.rag.ingestion.ingest_pipeline import IngestionPipeline

from app.rag.embeddings.embedding_pipeline import EmbeddingPipeline
from app.rag.embeddings.sentence_transformer_embedding import (
    SentenceTransformerEmbedding,
)

from app.rag.cache.joblib_cache import JoblibCache

from app.rag.vector_store.chroma_vector_store import ChromaVectorStore
from app.rag.pipeline.index_pipeline import IndexPipeline


print("=" * 70)
print("STEP 1 : INGESTION")
print("=" * 70)

ingestion = IngestionPipeline(
    loader=MarkdownLoader("data/rag"),
    chunker=ParentChildChunker(),
    cache=JoblibCache(),
).run()

print(f"Documents     : {len(ingestion.documents)}")
print(f"Parent Chunks : {len(ingestion.parent_chunks)}")
print(f"Child Chunks  : {len(ingestion.child_chunks)}")


print("\n" + "=" * 70)
print("STEP 2 : EMBEDDING")
print("=" * 70)

embedding = EmbeddingPipeline(
    embedding_model=SentenceTransformerEmbedding(),
    cache=JoblibCache(),
).run(ingestion)

print(f"Embedded Chunks : {len(embedding.embedded_chunks)}")
print(
    f"Embedding Dimension : "
    f"{len(embedding.embedded_chunks[0].embedding)}"
)


print("\n" + "=" * 70)
print("STEP 3 : CHROMA INDEX")
print("=" * 70)

vector_store = ChromaVectorStore()

# Start fresh for testing
vector_store.reset()

index_pipeline = IndexPipeline(
    vector_store=vector_store,
)

index_result = index_pipeline.run(
    embedding
)

print(f"Collection Name : {index_result.collection_name}")
print(f"Indexed Vectors : {index_result.total_vectors}")


print("\n" + "=" * 70)
print("STEP 4 : VERIFY CHROMA")
print("=" * 70)

count = vector_store.collection.count()

print(f"Vectors inside Chroma : {count}")

assert count == len(embedding.embedded_chunks)

print("\n✅ Indexing Successful!")