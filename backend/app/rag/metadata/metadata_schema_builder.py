from collections import defaultdict

from app.rag.metadata.metadata_schema import (
    MetadataSchema,
)


class MetadataSchemaBuilder:

    def build(

        self,

        parent_chunks,

    ) -> MetadataSchema:

        #
        # Every metadata field discovered
        #

        fields = set()

        #
        # Every value discovered for every field
        #

        values = defaultdict(set)

        for parent in parent_chunks:

            metadata = parent.metadata

            for key, value in metadata.items():

                #
                # Skip None
                #

                if value is None:

                    continue

                #
                # Register discovered field
                #

                fields.add(key)

                #
                # Lists
                #

                if isinstance(value, list):

                    for item in value:

                        values[key].add(str(item))

                #
                # Ignore nested dictionaries
                #

                elif isinstance(value, dict):

                    continue

                #
                # Everything else
                #

                else:

                    values[key].add(str(value))

        return MetadataSchema(

            fields=fields,

            values=dict(values),

        )