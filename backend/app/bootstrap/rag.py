from app.bootstrap.llm import get_llm
from app.bootstrap.schema.rag_services import RAGServices

from app.rag.loader.multi_loader import MultiLoader
from app.rag.loader.markdown_loader import MarkdownLoader
from app.rag.loader.pdf_loader import PdfLoader
from app.rag.loader.csv_loader import CsvLoader
from app.rag.loader.json_loader import JsonLoader

from app.rag.chunking.parent_child_chunker import ParentChildChunker
from app.rag.ingestion.ingest_pipeline import IngestionPipeline

from app.rag.embeddings.sentence_transformer_embedding import SentenceTransformerEmbedding
from app.rag.vector_store.chroma_vector_store import ChromaVectorStore

from app.rag.bm25.bm25_index import BM25Index

from app.rag.retrieval.chroma_retriever import ChromaRetriever
from app.rag.retrieval.bm25_retriever import BM25Retriever
from app.rag.retrieval.hybrid_retriever import HybridRetriever
from app.rag.retrieval.multi_query_retriever import MultiQueryRetriever
from app.rag.retrieval.rrf import ReciprocalRankFusion
from app.rag.retrieval.retrieval_pipeline import RetrievalPipeline

from app.rag.reranker.cross_encoder_reranker import CrossEncoderReranker

from app.rag.multi_query.llm_multi_query_generator import LLMMultiQueryGenerator

from app.rag.decomposition.decomposition_pipeline import DecompositionPipeline
from app.rag.decomposition.llm_query_decomposer import LLMQueryDecomposer

from app.rag.context_compression.child_context_compressor import ChildContextCompressor
from app.rag.context_compression.context_compression_pipeline import ContextCompressionPipeline

from app.rag.prompts.default_prompt_builder import DefaultPromptBuilder
from app.rag.generation.answer_generator import AnswerGenerator
from app.rag.generation.answer_pipeline import AnswerPipeline


def build_rag():

    llm = get_llm()

    ingestion = IngestionPipeline(

        loader=MultiLoader(

            loaders=[

                MarkdownLoader("data/rag"),

                PdfLoader("data/pdf"),

                CsvLoader("data/csv"),

                JsonLoader("data/json"),

            ]

        ),

        chunker=ParentChildChunker(),

    ).run()

    bm25 = BM25Index()

    bm25.build(

        ingestion.child_chunks

    )

    hybrid = HybridRetriever(

        dense_retriever=ChromaRetriever(

            vector_store=ChromaVectorStore(),

        ),

        sparse_retriever=BM25Retriever(

            bm25,

        ),

        fusion=ReciprocalRankFusion(),

    )

    retriever = MultiQueryRetriever(

        embedding_model=SentenceTransformerEmbedding(),

        generator=LLMMultiQueryGenerator(

            llm=llm,

        ),

        retriever=hybrid,

        fusion=ReciprocalRankFusion(),

    )

    retrieval_pipeline = RetrievalPipeline(

        retriever=retriever,

        reranker=CrossEncoderReranker(),

        decomposition_pipeline=DecompositionPipeline(

            decomposer=LLMQueryDecomposer(

                llm=llm,

            )

        ),

    )

    compression = ContextCompressionPipeline(

        compressor=ChildContextCompressor(),

    )

    answer_generator = AnswerGenerator(

        prompt_builder=DefaultPromptBuilder(),

        llm=llm,

    )

    pipeline = AnswerPipeline(

        retrieval_pipeline=retrieval_pipeline,

        context_compression_pipeline=compression,

        answer_generator=answer_generator,

    )

    return RAGServices(

        pipeline=pipeline,

        ingestion=ingestion,

    )