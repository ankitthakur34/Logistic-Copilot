from app.rag.loader.markdown_loader import MarkdownLoader
from app.rag.chunking.parent_child_chunker import ParentChildChunker
from app.rag.ingestion.ingest_pipeline import IngestionPipeline

from app.rag.embeddings.embedding_pipeline import EmbeddingPipeline
from app.rag.embeddings.sentence_transformer_embedding import SentenceTransformerEmbedding

from app.rag.cache.joblib_cache import JoblibCache


ingestion = IngestionPipeline(
    loader=MarkdownLoader("data/rag"),
    chunker=ParentChildChunker(),
    cache=JoblibCache(),
).run()


embedding = EmbeddingPipeline(
    embedding_model=SentenceTransformerEmbedding(),
    cache=JoblibCache(),
).run(ingestion)


print(len(embedding.embedded_chunks))

print(
    len(
        embedding.embedded_chunks[0].embedding
    )
)
