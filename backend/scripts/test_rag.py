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

from app.rag.prompts.default_prompt_builder import (
    DefaultPromptBuilder,
)

from app.rag.generation.answer_generator import (
    AnswerGenerator,
)

from app.rag.generation.answer_pipeline import (
    AnswerPipeline,
)

from app.rag.context_compression.child_context_compressor import (
    ChildContextCompressor,
)

from app.rag.context_compression.context_compression_pipeline import (
    ContextCompressionPipeline,
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
# CONTEXT COMPRESSION
###############################################################################

compression_pipeline = ContextCompressionPipeline(

    compressor=ChildContextCompressor(),

)


###############################################################################
# ANSWER GENERATOR
###############################################################################

answer_generator = AnswerGenerator(

    prompt_builder=DefaultPromptBuilder(),

    llm=GroqLLM(),

)


###############################################################################
# ANSWER PIPELINE
###############################################################################

pipeline = AnswerPipeline(

    retrieval_pipeline=retrieval_pipeline,
    # context compression pipeline to compress the retrieval results before generating the answer
    context_compression_pipeline=compression_pipeline,

    answer_generator=answer_generator,

)


###############################################################################
# QUESTION
###############################################################################

question = "Any updates on MV Maersk Horizon?"


questions = [

    "Why is shipment SHP0007 delayed?",

    "Why is Apple's refrigerated shipment delayed?",

    "Show me the Rotterdam weather issue.",

    "Any update on vessel Maersk Horizon?",

    "Email regarding SHP0010",

    "High priority emails for Samsung India",

    "Incidents at Rotterdam",

]


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