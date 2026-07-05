from app.rag.loader.markdown_loader import MarkdownLoader
from app.rag.chunking.parent_child_chunker import ParentChildChunker
from app.rag.ingestion.ingest_pipeline import IngestionPipeline

from app.rag.embeddings.embedding_pipeline import EmbeddingPipeline
from app.rag.embeddings.sentence_transformer_embedding import (
    SentenceTransformerEmbedding,
)

print("=" * 80)
print("STEP 1 : INGESTION")
print("=" * 80)

ingestion = IngestionPipeline(
    loader=MarkdownLoader("data/rag"),
    chunker=ParentChildChunker(),
).run()

print("Documents :", len(ingestion.documents))
print("Parents   :", len(ingestion.parent_chunks))
print("Children  :", len(ingestion.child_chunks))

print()

print("=" * 80)
print("STEP 2 : EMBEDDING")
print("=" * 80)

embeddings = EmbeddingPipeline(
    embedding_model=SentenceTransformerEmbedding(),
).run(
    ingestion.child_chunks
)

print("Embeddings :", len(embeddings))
print("Dimension  :", len(embeddings[0]))