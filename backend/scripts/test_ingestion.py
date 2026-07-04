from app.rag.loader.markdown_loader import MarkdownLoader
from app.rag.chunking.parent_child_chunker import ParentChildChunker
from app.rag.cache.joblib_cache import JoblibCache
from app.rag.ingestion.ingest_pipeline import IngestionPipeline


pipeline = IngestionPipeline(
    loader=MarkdownLoader("data/rag"),
    chunker=ParentChildChunker(),
    cache=JoblibCache(),
)

result = pipeline.run()

print()

print("=" * 60)
print("INGESTION SUMMARY")
print("=" * 60)

print(f"Documents      : {len(result.documents)}")
print(f"Parent Chunks  : {len(result.parent_chunks)}")
print(f"Child Chunks   : {len(result.child_chunks)}")
print(f"Parent Lookup  : {len(result.parent_lookup)}")
print(f"Child Lookup   : {len(result.child_lookup)}")

print("\nFirst Parent")
print(result.parent_chunks[0].id)

print("\nFirst Child")
print(result.child_chunks[0].id)

print("\nParent from Lookup")
print(
    result.parent_lookup[
        result.child_chunks[0].parent_id
    ].id
)

print("\nChild from Lookup")
print(
    result.child_lookup[
        result.child_chunks[0].id
    ].id
)