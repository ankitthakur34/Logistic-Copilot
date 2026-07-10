from app.rag.metadata.metadata_result import (
    MetadataResult,
)

from app.rag.metadata.metadata_schema import (
    MetadataSchema,
)

from app.rag.metadata.metadata_matcher import (
    MetadataMatcher,
)


class MetadataValidator:

    def __init__(

        self,

        schema: MetadataSchema,

    ):

        self.schema = schema

    def validate(

        self,

        metadata: MetadataResult,

    ) -> MetadataResult:

        validated = MetadataResult()

        #
        # Iterate over extracted metadata
        #

        for field_name, value in metadata.to_dict().items():

            #
            # Empty
            #

            if value is None:

                continue

            #
            # Unknown field
            #

            if not self.schema.has_field(

                field_name,

            ):

                continue

            allowed_values = (

                self.schema.allowed_values(
                    field_name,
                )
            )

            #
            # No catalog values
            #

            if not allowed_values:

                validated.set(

                    field_name,

                    value,

                )

                continue

            #
            # Exact match
            #

            if value in allowed_values:

                validated.set(

                    field_name,

                    value,

                )

                continue

            #
            # Fuzzy match
            #

            matched = MetadataMatcher.match(

                value=value,

                candidates=list(
                    allowed_values
                ),

            )

            if matched:

                validated.set(

                    field_name,

                    matched,

                )

        return validated