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

from app.rag.prompts.cargo_prompt_builder import (
    CargoPromptBuilder,
)


QUESTION = "Why is shipment SHP0007 delayed?"


ingestion = IngestionPipeline(
    loader=MarkdownLoader("data/rag"),
    chunker=ParentChildChunker(),
).run()


retrieval = RetrievalPipeline(
    embedding_model=SentenceTransformerEmbedding(),
    retriever=ChromaRetriever(
        vector_store=ChromaVectorStore(),
    ),
).run(
    question=QUESTION,
    ingestion=ingestion,
)


context = DefaultContextBuilder().build(
    retrieval
)


prompt = CargoPromptBuilder().build(
    question=QUESTION,
    context=context,
)


print("=" * 80)
print("SYSTEM PROMPT")
print("=" * 80)

print(prompt.system_prompt)

print()

print("=" * 80)
print("USER PROMPT")
print("=" * 80)

print(prompt.user_prompt)

print()

print("=" * 80)
print("FULL PROMPT")
print("=" * 80)

print(prompt.full_prompt)