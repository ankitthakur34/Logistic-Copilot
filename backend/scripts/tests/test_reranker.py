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

from app.rag.retrieval.multi_query_retriever import (
    MultiQueryRetriever,
)

from app.rag.retrieval.rrf import (
    ReciprocalRankFusion,
)

from app.rag.retrieval.retrieval_pipeline import (
    RetrievalPipeline,
)

from app.rag.reranker.cross_encoder_reranker import (
    CrossEncoderReranker,
)

from app.rag.multi_query.llm_multi_query_generator import (
    LLMMultiQueryGenerator,
)

from app.rag.llm.groq_llm import (
    GroqLLM,
)


###############################################################################
# INGESTION
###############################################################################

ingestion = IngestionPipeline(

    loader=MarkdownLoader("data/rag"),

    chunker=ParentChildChunker(),

).run()


###############################################################################
# BM25
###############################################################################

bm25 = BM25Index()

bm25.build(
    ingestion.child_chunks,
)


###############################################################################
# HYBRID RETRIEVER
###############################################################################

hybrid_retriever = HybridRetriever(

    dense_retriever=ChromaRetriever(

        vector_store=ChromaVectorStore(),

    ),

    sparse_retriever=BM25Retriever(

        bm25,

    ),

    fusion=ReciprocalRankFusion(),

)


###############################################################################
# MULTI QUERY RETRIEVER
###############################################################################

multi_query_retriever = MultiQueryRetriever(

    embedding_model=SentenceTransformerEmbedding(),

    generator=LLMMultiQueryGenerator(

        llm=GroqLLM(),

    ),

    retriever=hybrid_retriever,

    fusion=ReciprocalRankFusion(),

)


###############################################################################
# RETRIEVAL PIPELINE
###############################################################################

pipeline = RetrievalPipeline(

    retriever=multi_query_retriever,

    reranker=CrossEncoderReranker(),

)


###############################################################################
# TEST
###############################################################################

question = "Why is shipment SHP0007 delayed?"


result = pipeline.run(

    question=question,

    ingestion=ingestion,

    top_k=5,

)


###############################################################################
# PRINT RESULTS
###############################################################################

print("=" * 80)
print("QUESTION")
print("=" * 80)

print(question)

print()

print("=" * 80)
print("RERANKED CHILDREN")
print("=" * 80)

for rank, child in enumerate(

    result.children,

    start=1,

):

    print()

    print(f"Rank      : {rank}")

    print(f"Score     : {child.score:.4f}")

    print(f"ID        : {child.id}")

    print(f"Parent ID : {child.parent_id}")

    print()

    print(child.content[:300])


print()

print("=" * 80)
print("PARENTS")
print("=" * 80)

for parent in result.parents:

    print()

    print(parent.id)

    print()

    print(parent.content[:500])