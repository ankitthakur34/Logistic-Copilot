from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.rag.schema.document import (
    Document,
    ParentChunk,
    ChildChunk,
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

            file_id = (
                Path(document.metadata["path"])
                .with_suffix("")
                .as_posix()
                .replace("/", "_")
                .replace("\\", "_")
            )

            for parent_index, parent_text in enumerate(parents):

                parent_id = (
                    f"{file_id}_parent_{parent_index}"
                )

                parent = ParentChunk(
                    id=parent_id,
                    content=parent_text,
                    metadata=document.metadata.copy(),
                )

                parent_chunks.append(parent)

                children = self.child_splitter.split_text(
                    parent_text
                )

                for child_index, child_text in enumerate(children):

                    child = ChildChunk(
                        id=f"{parent_id}_child_{child_index}",
                        parent_id=parent_id,
                        content=child_text,
                        metadata=document.metadata.copy(),
                    )

                    child_chunks.append(child)

        return parent_chunks, child_chunks