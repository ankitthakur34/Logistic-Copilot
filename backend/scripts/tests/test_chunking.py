from app.rag.loader.json_loader import (
    JsonLoader,
)

from app.rag.chunking.parent_child_chunker import (
    ParentChildChunker,
)


docs = JsonLoader(
    "data/json"
).load()


parents, children = (

    ParentChildChunker()

    .chunk_documents(

        docs
    )

)


for p in parents:

    print()

    print(p.id)

    print(p.metadata)