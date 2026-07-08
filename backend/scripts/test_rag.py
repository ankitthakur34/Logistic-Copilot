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

from app.rag.prompts.cargo_prompt_builder import (
    CargoPromptBuilder,
)

from app.rag.generation.answer_generator import (
    AnswerGenerator,
)

from app.rag.generation.answer_pipeline import (
    AnswerPipeline,
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

retrieval_pipeline = RetrievalPipeline(

    retriever=multi_query_retriever,

    reranker=CrossEncoderReranker(),

)


###############################################################################
# ANSWER GENERATOR
###############################################################################

answer_generator = AnswerGenerator(

    prompt_builder=CargoPromptBuilder(),

    llm=GroqLLM(),

)


###############################################################################
# ANSWER PIPELINE
###############################################################################

pipeline = AnswerPipeline(

    retrieval_pipeline=retrieval_pipeline,

    answer_generator=answer_generator,

)


###############################################################################
# QUESTION
###############################################################################

question = "Why is shipment SHP0007 delayed?"


###############################################################################
# RUN
###############################################################################

result = pipeline.run(

    question=question,

    ingestion=ingestion,

    top_k=5,

)


###############################################################################
# PRINT
###############################################################################

print("=" * 80)
print("QUESTION")
print("=" * 80)

print(question)

print()

print("=" * 80)
print("ANSWER")
print("=" * 80)

print(result.answer)

print()

print("=" * 80)
print("MODEL")
print("=" * 80)

print(result.llm_result.model)

print()

print("=" * 80)
print("TOKEN USAGE")
print("=" * 80)

print(result.llm_result.usage)

print()

print("=" * 80)
print("SOURCES")
print("=" * 80)

for parent in result.retrieval.parents:

    print("-", parent.metadata.get("source"))

print()

print("=" * 80)
print("PARENTS")
print("=" * 80)

for parent in result.retrieval.parents:

    print()

    print(parent.id)

    print()

    print(parent.content[:500])