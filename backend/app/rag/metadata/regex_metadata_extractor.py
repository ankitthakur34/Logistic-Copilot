from app.rag.metadata.base_metadata_extractor import (
    BaseMetadataExtractor,
)

from app.rag.metadata.metadata_result import (
    MetadataResult,
)

from app.rag.metadata.metadata_regex import (
    PATTERNS,
)


class RegexMetadataExtractor(BaseMetadataExtractor):

    def extract(

        self,

        question: str,

    ) -> MetadataResult:

        metadata = MetadataResult()

        for field, pattern in PATTERNS.items():

            match = pattern.search(
                question,
            )

            if match:

                setattr(

                    metadata,

                    field,

                    match.group(0),

                )

        return metadata