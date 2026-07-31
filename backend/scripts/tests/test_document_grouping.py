from app.rag.loader.markdown_loader import MarkdownLoader
from app.rag.chunking.parent_child_chunker import ParentChildChunker
from app.rag.ingestion.ingest_pipeline import IngestionPipeline

from app.rag.evaluation.dataset.document_grouper import (
    DocumentGrouper,
)


ingestion = IngestionPipeline(

    loader=MarkdownLoader(

        "data/rag",

    ),

    chunker=ParentChildChunker(),

).run()


groups = (

    DocumentGrouper()

    .group(

        ingestion.parent_chunks,

    )

)

for idx, group in enumerate(groups):

    print()
    print("=" * 100)

    print(

        "GROUP",

        idx + 1,

    )

    print("=" * 100)

    for parent in group:

        print(

            parent.metadata.get(

                "source",

            )

        )