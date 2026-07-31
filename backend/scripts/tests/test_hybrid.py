from app.rag.loader.markdown_loader import MarkdownLoader
from app.rag.chunking.parent_child_chunker import ParentChildChunker
from app.rag.ingestion.ingest_pipeline import IngestionPipeline

from app.rag.embeddings.sentence_transformer_embedding import (
    SentenceTransformerEmbedding,
)

from app.rag.vector_store.chroma_vector_store import (
    ChromaVectorStore,
)

from app.rag.bm25.bm25_index import BM25Index

from app.rag.retrieval.chroma_retriever import (
    ChromaRetriever,
)

from app.rag.retrieval.bm25_retriever import (
    BM25Retriever,
)

from app.rag.retrieval.hybrid_retriever import (
    HybridRetriever,
)

from app.rag.retrieval.retrieval_pipeline import (
    RetrievalPipeline,
)


# ----------------------------
# Build ingestion
# ----------------------------

ingestion = IngestionPipeline(

    loader=MarkdownLoader("data/rag"),

    chunker=ParentChildChunker(),

).run()


# ----------------------------
# Build BM25
# ----------------------------

bm25 = BM25Index()

bm25.build(

    ingestion.child_chunks,

)


# ----------------------------
# Retrieval Pipeline
# ----------------------------

pipeline = RetrievalPipeline(

    embedding_model=SentenceTransformerEmbedding(),

    retriever=HybridRetriever(

        dense_retriever=ChromaRetriever(

            vector_store=ChromaVectorStore(),

        ),

        sparse_retriever=BM25Retriever(

            bm25_index=bm25,

        ),

    ),

)


# ----------------------------
# Ask question
# ----------------------------

result = pipeline.run(

    question="Why is bill of landing?",

    ingestion=ingestion,

)


# ----------------------------
# Children
# ----------------------------

print("=" * 80)
print("Retrieved Children")
print("=" * 80)

for child in result.children:

    print()

    print("Score     :", child.score)

    print("ID        :", child.id)

    print("Parent ID :", child.parent_id)

    print(child.content[:250])


# ----------------------------
# Parents
# ----------------------------

print()

print("=" * 80)
print("Retrieved Parents")
print("=" * 80)

for parent in result.parents:

    print()

    print(parent.id)

    print(parent.content[:500])