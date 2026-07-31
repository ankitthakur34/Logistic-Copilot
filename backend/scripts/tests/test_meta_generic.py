from app.rag.metadata.metadata_filter import (
    MetadataFilter,
)

from app.rag.metadata.metadata_result import (
    MetadataResult,
)

metadata = MetadataResult()

metadata.set(
    "customer",
    "Samsung India",
)

metadata.set(
    "priority",
    "High",
)

print()

print(metadata)

print()

print(

    MetadataFilter.to_chroma_where(

        metadata,

    )

)