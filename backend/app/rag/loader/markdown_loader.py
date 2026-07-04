from pathlib import Path

from app.rag.loader.base_loader import BaseLoader
from app.rag.schema.document import Document


class MarkdownLoader(BaseLoader):

    def __init__(self, root_path: str):

        self.root_path = Path(root_path)

    def load(self) -> list[Document]:

        documents = []

        markdown_files = self.root_path.rglob("*.md")

        for file in markdown_files:

            content = file.read_text(
                encoding="utf-8"
            )

            metadata = {
                "source": file.name,
                "folder": file.parent.name,
                "path": str(file),
            }

            document = Document(
                content=content,
                metadata=metadata,
            )

            documents.append(document)

        return documents