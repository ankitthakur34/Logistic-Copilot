from app.rag.loader.markdown_loader import MarkdownLoader
from app.rag.chunking.parent_child_chunker import ParentChildChunker
from app.rag.ingestion.ingest_pipeline import IngestionPipeline

from app.rag.embeddings.sentence_transformer_embedding import (
    SentenceTransformerEmbedding,
)

from app.rag.vector_store.chroma_vector_store import (
    ChromaVectorStore,
)

from app.rag.metadata.regex_metadata_extractor import (
    RegexMetadataExtractor,
)

from app.rag.metadata.metadata_filter import (
    MetadataFilter,
)


question = "Why is shipment SHP0007 delayed?"


ingestion = IngestionPipeline(

    loader=MarkdownLoader("data/rag"),

    chunker=ParentChildChunker(),

).run()


extractor = RegexMetadataExtractor()

metadata = extractor.extract(question)

print("=" * 80)
print("METADATA")
print("=" * 80)

print(metadata)


where = MetadataFilter.to_chroma_where(
    metadata,
)

print()

print("=" * 80)
print("WHERE")
print("=" * 80)

print(where)


embedding = SentenceTransformerEmbedding().embed_query(
    question,
)

result = ChromaVectorStore().search(

    query_embedding=embedding,

    where=where,

    top_k=10,

)


print()

print("=" * 80)
print("RESULTS")
print("=" * 80)

for idx, chunk_id in enumerate(result.ids):

    chunk = ingestion.child_lookup[chunk_id]

    print()

    print(f"Rank      : {idx+1}")
    print(f"ID        : {chunk.id}")
    print(f"Shipment  : {chunk.metadata.get('shipment')}")
    print(f"Source    : {chunk.metadata.get('source')}")
    print()
    print(chunk.content[:200])