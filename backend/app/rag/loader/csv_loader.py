import pandas as pd
from pathlib import Path

from app.rag.loader.base_loader import BaseLoader
from app.rag.schema.document import Document
from app.rag.utils.metadata_normalizer import (
    normalize_metadata,
)


class CsvLoader(BaseLoader):

    def __init__(self, root_path):

        self.root_path = Path(
            root_path
        )

    def load(self):

        documents = []

        files = self.root_path.rglob(
            "*.csv"
        )

        for file in files:

            df = pd.read_csv(
                file
            )

            for idx, row in df.iterrows():

                row_dict = (
                    row.to_dict()
                )

                content = "\n".join(

                    f"{k}: {v}"

                    for k, v
                    in row_dict.items()
                )

                metadata = {

                    "loader": "csv",

                    "source": file.name,

                    "row": idx,

                    "path": str(file),

                    **row_dict,
                }

                metadata = (
                    normalize_metadata(
                        metadata
                    )
                )

                documents.append(

                    Document(

                        content=content,

                        metadata=metadata,
                    )
                )

        return documents