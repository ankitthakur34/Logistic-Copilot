from app.rag.loader.markdown_loader import MarkdownLoader
from app.rag.chunking.parent_child_chunker import ParentChildChunker
from app.rag.ingestion.ingest_pipeline import IngestionPipeline

from app.rag.llm.groq_llm import (
    GroqLLM,
)

from app.rag.metadata.regex_metadata_extractor import (
    RegexMetadataExtractor,
)

# from app.rag.metadata.dictionary_metadata_extractor import DictionaryMetadataExtractor


from app.rag.metadata.llm_metadata_extractor import (
    LLMMetadataExtractor,
)

from app.rag.metadata.metadata_extraction_pipeline import (
    MetadataExtractionPipeline,
)


###############################################################################
# INGESTION
###############################################################################

ingestion = IngestionPipeline(

    loader=MarkdownLoader("data/rag"),

    chunker=ParentChildChunker(),

).run()


###############################################################################
# BUILD PIPELINE
###############################################################################

pipeline = MetadataExtractionPipeline(

    regex_extractor=RegexMetadataExtractor(),

    # dictionary_extractor=DictionaryMetadataExtractor(),

    llm_extractor=LLMMetadataExtractor(

        llm=GroqLLM(),

    ),

)


###############################################################################
# QUESTIONS
###############################################################################

questions = [

    "Why is shipment SHP0007 delayed?",

    "Why is Apple's refrigerated shipment delayed?",

    "Show me the Rotterdam weather issue.",

    "Any update on vessel Maersk Horizon?",

    "Email regarding SHP0010",

    "High priority emails for Samsung India",

    "Incidents at Rotterdam",

]


###############################################################################
# TEST
###############################################################################

for question in questions:

    print("=" * 80)
    print("QUESTION")
    print("=" * 80)

    print(question)
    print()

    ###########################################################################
    # REGEX
    ###########################################################################

    regex = pipeline.regex_extractor.extract(
        question,
    )

    print("-" * 80)
    print("REGEX RESULT")
    print("-" * 80)

    print(regex)
    print()

    ###########################################################################
    # FINAL PIPELINE
    ###########################################################################

    metadata = pipeline.extract(

        question=question,

        ingestion=ingestion,

    )

    print("-" * 80)
    print("FINAL METADATA")
    print("-" * 80)

    print(metadata)
    print()