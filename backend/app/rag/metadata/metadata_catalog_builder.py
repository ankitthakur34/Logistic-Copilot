from collections import defaultdict

from app.rag.metadata.metadata_catalog import MetadataCatalog

from app.rag.metadata.metadata_config import (
    FILTERABLE_FIELDS,
)


class MetadataCatalogBuilder:

    #
    # Only these metadata fields are allowed
    #

    def build(

        self,

        parent_chunks,

    ) -> MetadataCatalog:

        catalog = defaultdict(set)

        for parent in parent_chunks:

            metadata = parent.metadata

            for key, value in metadata.items():

                if key not in FILTERABLE_FIELDS:
                    continue

                if value is None:
                    continue

                if isinstance(value, list):

                    for item in value:

                        catalog[key].add(str(item))

                elif isinstance(value, dict):

                    continue

                else:

                    catalog[key].add(str(value))

        return MetadataCatalog(

            allowed_fields=FILTERABLE_FIELDS,

            allowed_values=dict(catalog),

        )