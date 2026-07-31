from app.rag.loader.markdown_loader import MarkdownLoader
from app.rag.chunking.parent_child_chunker import ParentChildChunker

loader = MarkdownLoader("data/rag")

documents = loader.load()

chunker = ParentChildChunker()

parents, children = chunker.chunk_documents(documents)

print(f"Documents : {len(documents)}")
print(f"Parents   : {len(parents)}")
print(f"Children  : {len(children)}")

print("\nFirst Parent")
print("=" * 60)
print(parents[0].id)
print(parents[0].metadata)
print(parents[0].content[:300])

print("\nFirst Child")
print("=" * 60)
print(children[0].id)
print(children[0].parent_id)
print(children[0].content)