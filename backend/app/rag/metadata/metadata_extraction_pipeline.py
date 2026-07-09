from app.rag.metadata.metadata_schema_builder import (
    MetadataSchemaBuilder,
)

from app.rag.metadata.metadata_validator import (
    MetadataValidator,
)

from app.rag.metadata.metadata_result import (
    MetadataResult,
)


class MetadataExtractionPipeline:

    def __init__(

        self,

        regex_extractor,

        dictionary_extractor,

        llm_extractor,

    ):

        self.regex_extractor = regex_extractor

        self.dictionary_extractor = dictionary_extractor

        self.llm_extractor = llm_extractor

        self.schema = None

        self.validator = None

    def prepare(

        self,

        ingestion,

    ):

        #
        # Already prepared
        #

        if self.validator is not None:

            return

        if ingestion is None:

            raise ValueError(

                "Ingestion is required to build metadata schema."

            )

        self.schema = MetadataSchemaBuilder().build(

            ingestion.parent_chunks,

        )

        self.validator = MetadataValidator(

            self.schema,

        )

    def merge(

        self,

        first: MetadataResult,

        second: MetadataResult,

    ) -> MetadataResult:

        #
        # Add values from second
        # only if first doesn't have them.
        #

        for field, value in second.to_dict().items():

            if value is None:

                continue

            if first.get(field) is None:

                first.set(

                    field,

                    value,

                )

        return first

    def extract(

        self,

        question: str,

        ingestion,

    ) -> MetadataResult:

        self.prepare(

            ingestion,

        )

        #
        # Regex extraction
        #

        regex_metadata = (

            self.regex_extractor.extract(

                question,

            )

        )

        #
        # Dictionary extraction
        #

        dictionary_metadata = (

            self.dictionary_extractor.extract(

                question,

                self.schema,

            )

        )

        #
        # Merge both
        #

        metadata = self.merge(

            regex_metadata,

            dictionary_metadata,

        )

        #
        # Use LLM only if needed
        #

        if metadata.is_empty():

            print()
            print(">>>> USING LLM <<<<")

            metadata = (

                self.llm_extractor.extract(

                    question,

                    self.schema,

                )

            )

        else:

            print()
            print(">>>> USING REGEX/DICTIONARY <<<<")

        print(metadata)
        print()

        return self.validator.validate(

            metadata,

        )