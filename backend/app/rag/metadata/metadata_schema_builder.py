from collections import defaultdict

from app.rag.metadata.metadata_schema import (
    MetadataSchema,
)


NON_QUERY_FIELDS = {

     "path",
    "source",
    "folder",
    "version",

    "tags",

    "title",

    "subject",

    "from",

    "to",
    "status"

}


class MetadataSchemaBuilder:

    def build(

        self,

        parent_chunks,

    ) -> MetadataSchema:

        catalog = defaultdict(set)

        value_to_fields = defaultdict(set)

        normalized_values = {}

        for parent in parent_chunks:

            metadata = parent.metadata

            for key, value in metadata.items():

                if value is None:
                    continue

                #
                # List values
                #

                if isinstance(value, list):

                    for item in value:

                        value_str = str(item)

                        catalog[key].add(
                            value_str,
                        )

                        value_to_fields[
                            value_str.lower()
                        ].add(
                            key,
                        )

                        normalized_values[
                            value_str.lower()
                        ] = value_str

                #
                # Ignore nested dicts
                #

                elif isinstance(value, dict):

                    continue

                #
                # Normal values
                #

                else:

                    value_str = str(value)

                    catalog[key].add(
                        value_str,
                    )

                    value_to_fields[
                        value_str.lower()
                    ].add(
                        key,
                    )

                    normalized_values[
                        value_str.lower()
                    ] = value_str

        #
        # Build queryable fields
        #

        queryable_fields = set()

        for field in catalog.keys():

            if field.lower() in NON_QUERY_FIELDS:

                continue

            queryable_fields.add(
                field,
            )

        return MetadataSchema(

            fields=set(
                catalog.keys(),
            ),

            values=dict(
                catalog,
            ),

            value_to_fields=dict(
                value_to_fields,
            ),

            normalized_values=normalized_values,

            queryable_fields=queryable_fields,

        )