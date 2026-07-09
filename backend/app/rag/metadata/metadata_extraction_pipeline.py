

from app.rag.metadata.metadata_catalog_builder import MetadataCatalogBuilder
from app.rag.metadata.metadata_validator import MetadataValidator


class MetadataExtractionPipeline:

    def __init__(

        self,

        regex_extractor,

        llm_extractor,

    ):

        self.regex_extractor = regex_extractor

        self.llm_extractor = llm_extractor

        self.catalog = None

        self.validator = None


    def prepare(

        self,

        ingestion,

    ):

        if self.validator is not None:
            return

        if ingestion is None:

            raise ValueError(
                "Ingestion is required to build MetadataCatalog."
            )

        self.catalog = MetadataCatalogBuilder().build(
            ingestion.parent_chunks,
        )

        self.validator = MetadataValidator(
            self.catalog,
        )


    def extract(

        self,

        question,

        ingestion,

    ):

        self.prepare(
            ingestion,
        )

        metadata = self.regex_extractor.extract(
            question,
        )

        if metadata.is_empty():

            print()
            print(">>>> USING LLM <<<<")

            metadata = self.llm_extractor.extract(
                question,
            )

        else:

            print()
            print(">>>> USING REGEX <<<<")

        print(metadata)
        print()

        return self.validator.validate(
            metadata,
        )