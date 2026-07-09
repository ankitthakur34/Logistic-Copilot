from dataclasses import fields

from app.rag.metadata.metadata_result import (
    MetadataResult,
)

from app.rag.metadata.metadata_catalog import (
    MetadataCatalog,
)


class MetadataValidator:

    def __init__(

        self,

        catalog: MetadataCatalog,

    ):

        self.catalog = catalog

    def validate(

        self,

        metadata: MetadataResult,

    ) -> MetadataResult:

        #
        # Iterate over every field in MetadataResult
        #

        for field in fields(MetadataResult):

            name = field.name

            #
            # Skip helper methods/fields if any are added later
            #

            if name == "is_empty":
                continue

            value = getattr(

                metadata,

                name,

            )

            #
            # Nothing to validate
            #

            if value is None:
                continue

            #
            # Field isn't filterable
            #

            if name not in self.catalog.allowed_fields:

                setattr(

                    metadata,

                    name,

                    None,

                )

                continue

            #
            # No value catalog -> allow
            #

            allowed = self.catalog.allowed_values.get(
                name,
            )

            if not allowed:
                continue

            #
            # Value doesn't exist in our documents
            #

            if value not in allowed:

                setattr(

                    metadata,

                    name,

                    None,

                )

        return metadata