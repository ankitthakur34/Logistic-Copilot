from pathlib import Path
import yaml

from app.rag.loader.base_loader import BaseLoader
from app.rag.schema.document import Document
from app.rag.utils.metadata_normalizer import (
    normalize_metadata,
)


class MarkdownLoader(BaseLoader):

    def __init__(self, root_path: str):

        self.root_path = Path(root_path)

    def load(self):

        documents = []

        markdown_files = self.root_path.rglob("*.md")

        for file in markdown_files:

            raw_text = file.read_text(
                encoding="utf8"
            )

            frontmatter = {}
            content = raw_text

            if raw_text.startswith("---"):

                parts = raw_text.split(
                    "---",
                    2,
                )

                if len(parts) >= 3:

                    frontmatter = (
                        yaml.safe_load(
                            parts[1]
                        )
                        or {}
                    )

                    content = parts[2].strip()

            metadata = {

                "loader": "markdown",

                "source": file.name,

                "folder": file.parent.name,

                "path": str(file),

                **frontmatter,
            }

            documents.append(

                Document(

                    content=content,

                    metadata=normalize_metadata(
                        metadata
                    ),
                )
            )

        return documents