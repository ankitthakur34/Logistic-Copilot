from dataclasses import fields

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

        for field in fields(MetadataResult):

            field_name = field.name

            #
            # Skip helper methods
            #

            value = getattr(

                metadata,

                field_name,

            )

            if value is None:

                continue

            #
            # Unknown field
            #

            if not self.schema.has_field(

                field_name,

            ):

                setattr(

                    metadata,

                    field_name,

                    None,

                )

                continue

            #
            # Unknown value
            #

            allowed = self.schema.allowed_values(

                field_name,

            )

            if allowed and value not in allowed:

                setattr(

                    metadata,

                    field_name,

                    None,

                )

        return metadata