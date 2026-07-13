from pathlib import Path
import yaml

from app.rag.loader.base_loader import BaseLoader
from app.rag.schema.document import Document
from datetime import date, datetime


def normalize_metadata(metadata: dict):

    normalized = {}

    for key, value in metadata.items():

        if isinstance(value, (date, datetime)):
            normalized[key] = value.isoformat()

        else:
            normalized[key] = value

    return normalized


class MarkdownLoader(BaseLoader):

    def __init__(self, root_path: str):

        self.root_path = Path(root_path)

    def load(self) -> list[Document]:

        documents = []

        markdown_files = self.root_path.rglob("*.md")

        for file in markdown_files:

            raw_text = file.read_text(
                encoding="utf-8"
            )

            frontmatter = {}
            content = raw_text

            # -----------------------------
            # Parse YAML Front Matter
            # -----------------------------
            if raw_text.startswith("---"):

                parts = raw_text.split(
                    "---",
                    2,
                )

                if len(parts) >= 3:

                    try:

                        frontmatter = yaml.safe_load(
                            parts[1]
                        ) or {}

                        content = parts[2].strip()

                    except yaml.YAMLError:

                        print(
                            f"[WARNING] Invalid YAML in {file.name}"
                        )

            # -----------------------------
            # Metadata
            # -----------------------------
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
    metadata=normalize_metadata(metadata),
)

            )

        return documents