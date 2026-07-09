from app.rag.metadata.metadata_schema_builder import MetadataSchemaBuilder
from app.rag.ingestion.ingest_pipeline import IngestionPipeline
from app.rag.chunking.parent_child_chunker import ParentChildChunker
from app.rag.loader.markdown_loader import MarkdownLoader

ingestion = IngestionPipeline(

    loader=MarkdownLoader("data/rag"),

    chunker=ParentChildChunker(),

).run()

schema = MetadataSchemaBuilder().build(
    ingestion.parent_chunks,
)

print(schema.fields)

print(schema.has_field("customer"))

print(schema.has_field("abc"))

print(schema.allowed_values("shipment"))
print(schema.allowed_values("customer"))

print(schema.allowed_values("xyz"))