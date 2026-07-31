from app.rag.metadata.metadata_schema_builder import (
    MetadataSchemaBuilder,
)

from app.rag.metadata.metadata_result import (
    MetadataResult,
)

from app.rag.metadata.metadata_validator import (
    MetadataValidator,
)

from app.rag.ingestion.ingest_pipeline import IngestionPipeline


from app.rag.loader.markdown_loader import (
    MarkdownLoader,
)

from app.rag.loader.json_loader import (
    JsonLoader,
)

from app.rag.chunking.parent_child_chunker import (
    ParentChildChunker,
)


loader = JsonLoader(
    "data/json"
)

pipeline = IngestionPipeline(
    loader=loader,
    chunker=ParentChildChunker(),
)

ingestion = pipeline.run()

schema = MetadataSchemaBuilder().build(
    ingestion.parent_chunks
)

validator = MetadataValidator(
    schema
)


tests = [

    MetadataResult(
        values={
            "shipment": "SHP0102"
        }
    ),

    MetadataResult(
        values={
            "shipment_id": "SHP0102"
        }
    ),

    MetadataResult(
        values={
            "shipment_number": "SHP0102"
        }
    ),

]


for test in tests:

    print()
    print("=" * 80)

    print("INPUT")
    print(test)

    validated = validator.validate(
        test
    )

    print("VALIDATED")
    print(validated)