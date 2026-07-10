import re

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
    BaseMetadataExtractor
):

    def extract(

        self,

        question: str,

        schema: MetadataSchema,

    ) -> MetadataResult:

        metadata = MetadataResult()

        question_lower = question.lower()

        #
        # Longest first
        #

        values = sorted(

            schema.value_to_fields.keys(),

            key=len,

            reverse=True,

        )

        for value in values:

            #
            # Exact word match
            #

            pattern = rf"\b{re.escape(value)}\b"

            if not re.search(

                pattern,

                question_lower,

            ):

                continue

            candidate_fields = (

                schema.candidate_fields(
                    value,
                )
            )
            candidate_fields = {

    field

    for field in candidate_fields

    if field in schema.queryable_fields

}

            if not candidate_fields:

                continue

            #
            # Single field
            #

            if len(candidate_fields) == 1:

                field = next(

                    iter(
                        candidate_fields
                    )
                )

                metadata.set(

                    field,

                    schema.original_value(
                        value,
                    ),

                )

                continue

            #
            # Ambiguous fields
            #

            matched_field = None

            for field in candidate_fields:

                field_pattern = (

                    rf"\b{re.escape(field.lower())}\b"

                )

                if re.search(

                    field_pattern,

                    question_lower,

                ):

                    matched_field = field

                    break

            if matched_field:

                metadata.set(

                    matched_field,

                    schema.original_value(
                        value,
                    ),

                )

        return metadata