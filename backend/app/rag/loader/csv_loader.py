from pathlib import Path
import pandas as pd

from app.rag.loader.base_loader import BaseLoader
from app.rag.schema.document import Document


class CsvLoader(BaseLoader):

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

        csv_files = self.root_path.rglob(
            "*.csv"
        )

        for file in csv_files:

            df = pd.read_csv(
                file
            )

            for idx, row in df.iterrows():

                text_parts = []

                metadata = {

                    "loader": "csv",

                    "source": file.name,

                    "row": idx,

                    "path": str(file),

                }

                for col, value in row.items():

                    if pd.isna(value):

                        continue

                    text_parts.append(

                        f"{col}: {value}"

                    )

                    #
                    # Optional:
                    # put row values into metadata
                    #

                    metadata[

                        col.lower()

                    ] = str(value)

                content = "\n".join(

                    text_parts

                )

                documents.append(

                    Document(

                        content=content,

                        metadata=metadata,

                    )

                )

        return documents