from app.rag.loader.markdown_loader import MarkdownLoader
from app.rag.chunking.parent_child_chunker import ParentChildChunker
from app.rag.ingestion.ingest_pipeline import IngestionPipeline

from app.rag.bm25.bm25_index import BM25Index
from app.rag.retrieval.bm25_retriever import BM25Retriever


ingestion = IngestionPipeline(

    loader=MarkdownLoader("data/rag"),

    chunker=ParentChildChunker(),

).run()


bm25 = BM25Index()

bm25.build(
    ingestion.child_chunks,
)

result = BM25Retriever(bm25_index=bm25).retrieve(

    question="Why SHP0007 delayed?",

    top_k=5,

)

print("=" * 80)
print("RESULTS")
print("=" * 80)

for rank, (chunk_id, score) in enumerate(

    zip(result.ids, result.scores),

    start=1,

):

    print()

    print(f"Rank : {rank}")

    print(f"ID   : {chunk_id}")

    print(f"Score: {score:.4f}")