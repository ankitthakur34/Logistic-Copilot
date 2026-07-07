import re

from app.rag.metadata.base_metadata_extractor import (
    BaseMetadataExtractor,
)

from app.rag.metadata.metadata_result import (
    MetadataResult,
)


class RegexMetadataExtractor(
    BaseMetadataExtractor,
):

    SHIPMENT_PATTERN = re.compile(
        r"\bSHP\d+\b",
        re.IGNORECASE,
    )

    EMAIL_PATTERN = re.compile(
        r"\bEMAIL-\d+\b",
        re.IGNORECASE,
    )

    def extract(
        self,
        question: str,
    ) -> MetadataResult:

        result = MetadataResult()

        shipment = self.SHIPMENT_PATTERN.search(
            question,
        )

        if shipment:

            result.shipment = shipment.group().upper()

        email = self.EMAIL_PATTERN.search(
            question,
        )

        if email:

            result.email = email.group().upper()

        return result