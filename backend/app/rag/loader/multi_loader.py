from app.rag.loader.base_loader import BaseLoader
from app.rag.schema.document import Document


class MultiLoader(BaseLoader):

    def __init__(
        self,
        loaders: list[BaseLoader],
    ):

        self.loaders = loaders

    def load(
        self,
    ) -> list[Document]:

        documents = []

        for loader in self.loaders:

            docs = loader.load()

            documents.extend(
                docs
            )

        return documents