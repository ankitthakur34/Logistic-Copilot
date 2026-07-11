from datetime import datetime
import json
from pathlib import Path

from app.rag.evaluation.dataset.evaluation_dataset_loader import (

    EvaluationDatasetLoader,

)

from app.rag.evaluation.dataset.dataset_loader import (
    DatasetLoader,
)

from app.rag.evaluation.metrics.default_metrics import (
    build_metrics,
)

from app.rag.evaluation.runners.testcase_builder import (
    TestCaseBuilder,
)

from deepeval import evaluate
from deepeval.evaluate import DisplayConfig


###############################################################################
# IMPORT YOUR RAG
###############################################################################

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

from app.rag.decomposition.decomposition_pipeline import (
    DecompositionPipeline,
)

from app.rag.decomposition.llm_query_decomposer import (
    LLMQueryDecomposer,
)

###############################################################################
# BUILD RAG
###############################################################################

ingestion = IngestionPipeline(

    loader=MarkdownLoader("data/rag"),

    chunker=ParentChildChunker(),

).run()


bm25 = BM25Index()

bm25.build(

    ingestion.child_chunks,

)


hybrid_retriever = HybridRetriever(

    dense_retriever=ChromaRetriever(

        vector_store=ChromaVectorStore(),

    ),

    sparse_retriever=BM25Retriever(

        bm25,

    ),

    fusion=ReciprocalRankFusion(),

)


multi_query_retriever = MultiQueryRetriever(

    embedding_model=SentenceTransformerEmbedding(),

    generator=LLMMultiQueryGenerator(

        llm=GroqLLM(),

    ),

    retriever=hybrid_retriever,

    fusion=ReciprocalRankFusion(),

)


retrieval_pipeline = RetrievalPipeline(

    retriever=multi_query_retriever,

    reranker=CrossEncoderReranker(),

    decomposition_pipeline=(

        DecompositionPipeline(

            decomposer=LLMQueryDecomposer(

                llm=GroqLLM(
                    model="llama-3.1-8b-instant",
                ),

            )

        )

    )

)


compression_pipeline = ContextCompressionPipeline(

    compressor=ChildContextCompressor(),

)


answer_generator = AnswerGenerator(

    prompt_builder=DefaultPromptBuilder(),

    llm=GroqLLM(),

)


pipeline = AnswerPipeline(

    retrieval_pipeline=retrieval_pipeline,

    context_compression_pipeline=compression_pipeline,

    answer_generator=answer_generator,

)

###############################################################################
# LOAD DATASET
###############################################################################

dataset = (

    EvaluationDatasetLoader()

    .load(

        "app/rag/evaluation/dataset/generated/generated_dataset.json"

    )

)

dataset = dataset[:3]

print("================================" * 5)
print("DATASET RESULTS")
print("================================" * 5)
print(dataset)

metrics = build_metrics()

query_results = []

###############################################################################
# LOOP
###############################################################################

for sample in dataset:

    question = sample.question

    expected_answer = (

        sample.expected_answer

    )

    expected_sources = (

        sample.expected_sources

    )

    print()
    print("=" * 100)
    print("QUESTION")
    print("=" * 100)
    print(question)

    ##########################################################
    # RUN RAG
    ##########################################################

    rag_result = pipeline.run(

        question=question,

        ingestion=ingestion,

        top_k=5,

    )

    print()
    print("=" * 100)
    print("ANSWER")
    print("=" * 100)
    print(rag_result.answer)

    ##########################################################
    # BUILD TEST CASE
    ##########################################################

    test_case = TestCaseBuilder.build(

        question=question,

        expected_answer=expected_answer,

        actual_answer=rag_result.answer,

        retrieval=rag_result.retrieval,

    )

    ##########################################################
    # RUN EVAL
    ##########################################################

    try:

        result = evaluate(

        test_cases=[test_case],

        metrics=metrics,

    )

    except Exception as e:

        print()

        print("Evaluation Failed")

        print(e)

        continue

    ##########################################################
    # EXTRACT SCORES
    ##########################################################

    metric_results = []

    metrics_data = (

        result.test_results[0]

        .metrics_data

    )

    print()
    print("=" * 100)
    print("METRICS")
    print("=" * 100)

    for metric in metrics_data:

        print()

        print(

            metric.name,

            ":",

            round(

                metric.score,

                3,

            )

        )

        print(

            "Reason:",

            metric.reason,

        )

        metric_results.append(

            {

                "name": metric.name,

                "score": metric.score,

                "reason": metric.reason,

                "success": metric.success,

            }

        )

    ##########################################################
    # STORE QUERY RESULT
    ##########################################################

    actual_sources = [

    p.metadata.get(

        "source"

    )

    for p in rag_result.retrieval.parents

]
    
    expected_set = set(

    expected_sources

)

    actual_set = set(

    actual_sources

)
    
    print()
    print("=" * 100)
    print("EXPECTED SOURCES")
    print("=" * 100)

    for s in expected_sources:

        print("-", s)

    print()
    print("=" * 100)
    print("RETRIEVED SOURCES")
    print("=" * 100)

    for s in actual_sources:

        print("-", s)

    if expected_set:

        recall = (

        len(

            expected_set

            &

            actual_set

        )

        /

        len(

            expected_set

        )

    )

    else:

        recall = 1.0


    if actual_set:

        precision = (

        len(

            expected_set

            &

            actual_set

        )

        /

        len(

            actual_set

        )

    )

    else:

        precision = 1.0 

    print()
    print("=" * 100)
    print("RETRIEVAL")
    print("=" * 100)

    print(

    "Precision:",

    round(

        precision,

        3,

    )

)

    print(

    "Recall:",

    round(

        recall,

        3,

    )

)       
    
    query_results.append(

    {

        "question":

            question,

        "expected_answer":

            expected_answer,

        "actual_answer":

            rag_result.answer,

        "expected_sources":

            expected_sources,

        "actual_sources":

            actual_sources,

        "metrics": metric_results,

        "retrieval_precision": precision,

        "retrieval_recall": recall,    

    }

)

###############################################################################
# AVERAGES
###############################################################################

averages = {}

retrieval_precisions = []

retrieval_recalls = []


for query in query_results:

    retrieval_precisions.append(

        query[

            "retrieval_precision"

        ]

    )

    retrieval_recalls.append(

        query[

            "retrieval_recall"

        ]

    )

    for metric in query["metrics"]:

        name = metric["name"]

        averages.setdefault(

            name,

            []

        )

        averages[name].append(

            metric["score"]

        )

average_scores = {}

for name, scores in averages.items():

    average_scores[

    "Retrieval Precision"

] = round(

    sum(

        retrieval_precisions

    )

    /

    len(

        retrieval_precisions

    ),

    3,

)

average_scores[

    "Retrieval Recall"

] = round(

    sum(

        retrieval_recalls

    )

    /

    len(

        retrieval_recalls

    ),

    3,

)

print()
print("=" * 100)
print("AVERAGE SCORES")
print("=" * 100)

for name, score in average_scores.items():

    print(

        name,

        ":",

        score,

    )

###############################################################################
# SAVE REPORT
###############################################################################

report = {

    "average_scores":

        average_scores,

    "queries":

        query_results,

}

report_dir = Path(

    "app/rag/evaluation/reports"

)

report_dir.mkdir(

    parents=True,

    exist_ok=True,

)

timestamp = (

    datetime.now()

    .strftime(

        "%Y_%m_%d_%H_%M_%S"

    )

)

report_path = (

    report_dir

    /

    f"evaluation_{timestamp}.json"

)

with open(

    report_path,

    "w",

    encoding="utf8",

) as f:

    json.dump(

        report,

        f,

        indent=4,

        ensure_ascii=False,

    )

print()
print("=" * 100)
print("REPORT SAVED")
print("=" * 100)

print(report_path)