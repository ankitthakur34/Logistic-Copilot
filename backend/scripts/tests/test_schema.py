from app.rag.ingestion.ingest_pipeline import (
    IngestionPipeline,
)

from app.rag.loader.markdown_loader import (
    MarkdownLoader,
)

from app.rag.chunking.parent_child_chunker import (
    ParentChildChunker,
)

from app.rag.metadata.metadata_schema_builder import (
    MetadataSchemaBuilder,
)

from app.rag.metadata.dictionary_metadata_extractor import (
    DictionaryMetadataExtractor,
)


###############################################################################
# BUILD INGESTION
###############################################################################

ingestion = IngestionPipeline(

    loader=MarkdownLoader(

        "data/rag",

    ),

    chunker=ParentChildChunker(),

).run()


###############################################################################
# BUILD SCHEMA
###############################################################################

schema = MetadataSchemaBuilder().build(

    ingestion.parent_chunks,

)


###############################################################################
# EXTRACTOR
###############################################################################

extractor = DictionaryMetadataExtractor()


###############################################################################
# QUESTIONS
###############################################################################

questions = [

    "High priority emails for Samsung India",

    "High severity incidents",

    "Rotterdam weather issue",

    "Operations emails",

    "Tell me about SHP0007",

    "Any updates on MV Maersk Horizon?",

    "Customs incidents",

    "Weather reports",

]


###############################################################################
# TEST
###############################################################################

for question in questions:

    print()
    print("=" * 100)
    print("QUESTION")
    print("=" * 100)

    print(question)

    print()

    metadata = extractor.extract(

        question,

        schema,

    )

    print("-" * 100)
    print("METADATA")
    print("-" * 100)

    print(metadata)

    print()

    print("-" * 100)
    print("DICT")
    print("-" * 100)

    print(

        metadata.to_dict()

    )

    print()