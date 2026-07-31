from app.rag.loader import MarkdownLoader

loader = MarkdownLoader("data/rag")

documents = loader.load()

print(f"Loaded {len(documents)} documents")

for document in documents[:3]:

    print("=" * 50)

    print(document.metadata)

    print(document.content[:1500])