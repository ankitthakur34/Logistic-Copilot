from pathlib import Path
from typing import Counter

from langchain_text_splitters import RecursiveCharacterTextSplitter
from numpy import rint
from sqlalchemy.util import counter


from app.rag.schema.document import (
    Document,
    ParentChunk,
    ChildChunk
)


class ParentChildChunker:

    def __init__(
        self,
        parent_chunk_size: int = 1000,
        parent_overlap: int = 150,
        child_chunk_size: int = 250,
        child_overlap: int = 50,
    ):

        self.parent_splitter = RecursiveCharacterTextSplitter(
            chunk_size=parent_chunk_size,
            chunk_overlap=parent_overlap,
        )

        self.child_splitter = RecursiveCharacterTextSplitter(
            chunk_size=child_chunk_size,
            chunk_overlap=child_overlap,
        )

    def chunk_documents(
        self,
        documents: list[Document],
    ):

        parent_chunks = []
        child_chunks = []

        for document in documents:

            parents = self.parent_splitter.split_text(
                document.content
            )

            for parent_index, parent_text in enumerate(parents):

                file_id = (
        Path(document.metadata["path"])
    .with_suffix("")
    .as_posix()
    .replace("/", "_")
    .replace("\\", "_")
)

                parent_id = f"{file_id}_parent_{parent_index}"
                

                parent = ParentChunk(
                    id=parent_id,
                    content=parent_text,
                    metadata=document.metadata.copy(),
                )

                parent_chunks.append(parent)

                children = self.child_splitter.split_text(
                    parent_text
                )
                if document.metadata["source"] == "port_operations.md":

                    print("=" * 80)
                    print("Children Returned:", len(children))

                    for idx, text in enumerate(children):
                        print(f"\n----- Child {idx} -----")
                        print(repr(text))
                    print("\nEnumerate Test")

                    for idx, _ in enumerate(children):
                        print(idx)    

                for child_index, child_text in enumerate(children):
                    print(
    "Creating ->",
    parent_id,
    child_index,
)

                    child = ChildChunk(
                        id=f"{parent_id}_child_{child_index}",
                        parent_id=parent_id,
                        content=child_text,
                        metadata=document.metadata.copy(),
                    )

                    child_chunks.append(child)
                



        return parent_chunks, child_chunks