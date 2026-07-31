from app.rag.loader.markdown_loader import MarkdownLoader
from app.rag.chunking.parent_child_chunker import ParentChildChunker
from app.rag.ingestion.ingest_pipeline import IngestionPipeline

print("=" * 70)
print("INGESTION TEST")
print("=" * 70)

pipeline = IngestionPipeline(
    loader=MarkdownLoader("data/rag"),
    chunker=ParentChildChunker(),
)

result = pipeline.run()

print()

print("Documents :", len(result.documents))
print("Parents   :", len(result.parent_chunks))
print("Children  :", len(result.child_chunks))

print()

print("=" * 70)
print("FIRST DOCUMENT")
print("=" * 70)

print(result.documents[0].metadata)
print()
print(result.documents[0].content[:300])

print()

print("=" * 70)
print("FIRST PARENT")
print("=" * 70)

print(result.parent_chunks[0].id)
print(result.parent_chunks[0].metadata)
print()
print(result.parent_chunks[0].content[:300])

print()

print("=" * 70)
print("FIRST CHILD")
print("=" * 70)

print(result.child_chunks[0].id)
print(result.child_chunks[0].parent_id)
print(result.child_chunks[0].metadata)
print()
print(result.child_chunks[0].content[:300])