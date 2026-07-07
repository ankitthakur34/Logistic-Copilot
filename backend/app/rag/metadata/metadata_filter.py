from app.rag.metadata.metadata_result import MetadataResult


class MetadataFilter:

    @staticmethod
    def to_chroma_where(
        metadata: MetadataResult,
    ):

        where = {}

        if metadata.shipment:

            where["shipment"] = metadata.shipment

        if metadata.email:

            where["email_id"] = metadata.email

        return where