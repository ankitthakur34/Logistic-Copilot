from app.rag.loader.markdown_loader import MarkdownLoader
from app.rag.chunking.parent_child_chunker import ParentChildChunker
from app.rag.ingestion.ingest_pipeline import IngestionPipeline

from app.rag.embeddings.embedding_pipeline import (
    EmbeddingPipeline,
)
from app.rag.embeddings.sentence_transformer_embedding import (
    SentenceTransformerEmbedding,
)

from app.rag.vector_store.chroma_vector_store import (
    ChromaVectorStore,
)

from app.rag.pipeline.index_pipeline import (
    IndexPipeline,
)

print("=" * 70)
print("STEP 1 : INGESTION")
print("=" * 70)

ingestion = IngestionPipeline(
    loader=MarkdownLoader("data/rag"),
    chunker=ParentChildChunker(),
).run()

print(f"Documents : {len(ingestion.documents)}")
print(f"Parents   : {len(ingestion.parent_chunks)}")
print(f"Children  : {len(ingestion.child_chunks)}")

print()

print("=" * 70)
print("STEP 2 : EMBEDDINGS")
print("=" * 70)

embeddings = EmbeddingPipeline(
    embedding_model=SentenceTransformerEmbedding(),
).run(
    ingestion.child_chunks
)

print(f"Embeddings : {len(embeddings)}")
print(f"Dimension  : {len(embeddings[0])}")

print()

print("=" * 70)
print("STEP 3 : CHROMA INDEX")
print("=" * 70)

vector_store = ChromaVectorStore()



vector_store.reset()

IndexPipeline(
    vector_store=vector_store,
).run(
    child_chunks=ingestion.child_chunks,
    embeddings=embeddings,
)

print()

print("=" * 70)
print("STEP 4 : VERIFY CHROMA")
print("=" * 70)

print(
    "Vectors inside Chroma :",
    vector_store.count(),
)

print("\n✅ Indexing Successful!")