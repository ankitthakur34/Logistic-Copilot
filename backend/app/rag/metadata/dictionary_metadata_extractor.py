from app.rag.metadata.base_metadata_extractor import (
    BaseMetadataExtractor,
)

from app.rag.metadata.metadata_result import (
    MetadataResult,
)

from app.rag.metadata.metadata_schema import (
    MetadataSchema,
)


class DictionaryMetadataExtractor(
    BaseMetadataExtractor,
):

    def extract(

        self,

        question: str,

        schema: MetadataSchema,

    ) -> MetadataResult:

        metadata = MetadataResult()

        question_lower = question.lower()

        #
        # Iterate through every discovered metadata field
        #

        for field_name, values in schema.values.items():

            #
            # Ignore empty fields
            #

            if not values:

                continue

            #
            # Longest values first
            #

            sorted_values = sorted(

                values,

                key=len,

                reverse=True,

            )

            for value in sorted_values:

                if value.lower() in question_lower:

                    metadata.set(

                        field_name,

                        value,

                    )

                    #
                    # Stop after first match
                    #

                    break

        return metadata