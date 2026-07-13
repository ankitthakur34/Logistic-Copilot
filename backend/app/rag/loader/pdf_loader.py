from pathlib import Path
import fitz

from app.rag.loader.base_loader import BaseLoader
from app.rag.schema.document import Document


class PdfLoader(BaseLoader):

    def __init__(
        self,
        root_path: str,
    ):

        self.root_path = Path(
            root_path
        )

    def load(
        self,
    ) -> list[Document]:

        documents = []

        pdf_files = self.root_path.rglob(
            "*.pdf"
        )

        for file in pdf_files:

            pdf = fitz.open(
                file
            )

            for page_number in range(

                len(pdf)

            ):

                page = pdf.load_page(

                    page_number

                )

                text = page.get_text()

                if not text.strip():

                    continue

                metadata = {

                    "loader": "pdf",

                    "source": file.name,

                    "page": page_number + 1,

                    "path": str(file),

                }

                documents.append(

                    Document(

                        content=text,

                        metadata=metadata,

                    )

                )

        return documents