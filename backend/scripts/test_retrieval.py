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

ingestion = IngestionPipeline(
    loader=MarkdownLoader("data/rag"),
    chunker=ParentChildChunker(),
).run()

pipeline = RetrievalPipeline(
    embedding_model=SentenceTransformerEmbedding(),
    retriever=ChromaRetriever(
        vector_store=ChromaVectorStore(),
    ),
)

result = pipeline.run(
    question="Why is shipment SHP0007 delayed?",
    ingestion=ingestion,
)

print("=" * 80)
print("Retrieved Children")
print("=" * 80)

for child in result.children:

    print()

    print(child.score)

    print(child.id)

    print(child.parent_id)

    print(child.content[:250])

print()

print("=" * 80)
print("Retrieved Parents")
print("=" * 80)

for parent in result.parents:

    print()

    print(parent.id)

    print(parent.content[:500])