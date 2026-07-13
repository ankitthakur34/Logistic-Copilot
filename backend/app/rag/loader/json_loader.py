from pathlib import Path
import json

from app.rag.loader.base_loader import BaseLoader
from app.rag.schema.document import Document
from app.rag.utils.json_utils import flatten_json
from app.rag.utils.metadata_normalizer import (
    normalize_metadata,
)


class JsonLoader(BaseLoader):

    def __init__(self, root_path: str):

        self.root_path = Path(root_path)

    def load(self):

        documents = []

        files = self.root_path.rglob(
            "*.json"
        )

        for file in files:

            with open(
                file,
                encoding="utf8",
            ) as f:

                data = json.load(f)

            if not isinstance(
                data,
                list,
            ):
                data = [data]

            for idx, item in enumerate(data):

                flattened = flatten_json(
                    item
                )

                content = "\n".join(

                    f"{k}: {v}"

                    for k, v
                    in flattened.items()
                )

                metadata = {

                    "loader": "json",

                    "source": file.name,

                    "row": idx,

                    "path": str(file),
                }

                metadata.update(
                    flattened
                )

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