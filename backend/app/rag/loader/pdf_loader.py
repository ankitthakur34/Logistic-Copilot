import fitz
from pathlib import Path

from app.rag.loader.base_loader import BaseLoader
from app.rag.schema.document import Document

from app.rag.utils.metadata_normalizer import (
    normalize_metadata,
)


class PdfLoader(BaseLoader):

    def __init__(
        self,
        root_path: str,
    ):

        self.root_path = Path(
            root_path
        )

    def load(self):

        documents = []

        pdf_files = self.root_path.rglob(
            "*.pdf"
        )

        for file in pdf_files:

            pdf = fitz.open(file)

            for page_no in range(
                len(pdf)
            ):

                page = pdf.load_page(
                    page_no
                )

                text = page.get_text()

                metadata = {

                    "loader": "pdf",

                    "source": file.name,

                    "page": page_no,

                    "path": str(file),
                }

                metadata = (
                    normalize_metadata(
                        metadata
                    )
                )

                documents.append(

                    Document(

                        content=text,

                        metadata=metadata,
                    )

                )

        return documents