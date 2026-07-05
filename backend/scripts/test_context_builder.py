from app.rag.loader.markdown_loader import MarkdownLoader
from app.rag.chunking.parent_child_chunker import ParentChildChunker
from app.rag.ingestion.ingest_pipeline import IngestionPipeline

from app.rag.embeddings.sentence_transformer_embedding import (
    SentenceTransformerEmbedding,
)

from app.rag.vector_store.chroma_vector_store import (
    ChromaVectorStore,
)

from app.rag.retrieval.chroma_retriever import (
    ChromaRetriever,
)

from app.rag.retrieval.retrieval_pipeline import (
    RetrievalPipeline,
)

from app.rag.context.default_context_builder import (
    DefaultContextBuilder,
)

print("=" * 80)
print("STEP 1 : INGESTION")
print("=" * 80)

ingestion = IngestionPipeline(
    loader=MarkdownLoader("data/rag"),
    chunker=ParentChildChunker(),
).run()

print()

print("=" * 80)
print("STEP 2 : RETRIEVAL")
print("=" * 80)

pipeline = RetrievalPipeline(
    embedding_model=SentenceTransformerEmbedding(),
    retriever=ChromaRetriever(
        vector_store=ChromaVectorStore(),
    ),
)

retrieval = pipeline.run(
    question="Why is shipment SHP0007 delayed?",
    ingestion=ingestion,
)

print(f"Retrieved Parents : {len(retrieval.parents)}")
print()

print("=" * 80)
print("STEP 3 : CONTEXT BUILDER")
print("=" * 80)

builder = DefaultContextBuilder()

context = builder.build(retrieval)

print(f"Document Count : {context.document_count}")

print()

print("Sources")

for source in context.sources:
    print(f" - {source}")

print()

print("=" * 80)
print("FINAL CONTEXT")
print("=" * 80)

print(context.context)