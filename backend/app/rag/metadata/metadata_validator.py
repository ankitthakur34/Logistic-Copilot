from app.rag.metadata.metadata_result import (
    MetadataResult,
)

from app.rag.metadata.metadata_schema import (
    MetadataSchema,
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
            # Skip empty values
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

            #
            # Allowed values
            #

            allowed_values = self.schema.allowed_values(

                field_name,

            )

            #
            # If catalog exists,
            # validate against it.
            #

            if (

                allowed_values

                and

                value not in allowed_values

            ):

                continue

            validated.set(

                field_name,

                value,

            )

        return validated