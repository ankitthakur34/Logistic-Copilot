from pathlib import Path
import json

from app.rag.loader.base_loader import (
    BaseLoader,
)

from app.rag.schema.document import (
    Document,
)

from app.rag.utils.json_utils import (
    flatten_json,
)


class JsonLoader(BaseLoader):

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

        json_files = self.root_path.rglob(

            "*.json"

        )

        for file in json_files:

            with open(

                file,
                encoding="utf8",

            ) as f:

                data = json.load(

                    f

                )

            #
            # support list
            #

            if not isinstance(

                data,
                list,

            ):

                data = [

                    data

                ]

            for idx, item in enumerate(

                data

            ):

                if not isinstance(

                    item,
                    dict,

                ):

                    continue

                flattened = (

                    flatten_json(

                        item

                    )

                )

                content = "\n".join(

                    f"{k}: {v}"

                    for k, v

                    in flattened.items()

                )

                metadata = {

                    "loader":"json",

                    "source":file.name,

                    "row":idx,

                    "path":str(file),

                }

                #
                # optional:
                # add fields
                #

                for key, value in (

                    flattened.items()

                ):

                    metadata[

                        key.lower()

                    ] = str(

                        value

                    )

                documents.append(

                    Document(

                        content=content,

                        metadata=metadata,

                    )

                )

        return documents