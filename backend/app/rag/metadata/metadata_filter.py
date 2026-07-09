from dataclasses import fields

from app.rag.metadata.metadata_result import MetadataResult


class MetadataFilter:

    @staticmethod
    def to_chroma_where(
        metadata: MetadataResult,
    ):

        clauses = []

        for field in fields(MetadataResult):

            value = getattr(metadata, field.name)

            if value is None:
                continue

            clauses.append(
                {
                    field.name: value,
                }
            )

        #
        # No filters
        #

        if not clauses:

            return None

        #
        # Single filter
        #

        if len(clauses) == 1:

            return clauses[0]

        #
        # Multiple filters
        #

        return {

            "$and": clauses,

        }