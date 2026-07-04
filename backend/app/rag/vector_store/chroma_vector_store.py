import chromadb

from app.rag.schema.embedding_result import EmbeddingResult
from app.rag.vector_store.base_vector_store import BaseVectorStore


class ChromaVectorStore(BaseVectorStore):

    def __init__(
        self,
        collection_name: str = "cargo_ai",
        persist_directory: str = "./chroma_db",
    ):

        self._collection_name = collection_name

        self.client = chromadb.PersistentClient(
            path=persist_directory
        )

        self.collection = self.client.get_or_create_collection(
            name=self._collection_name
        )

    @property
    def collection_name(self) -> str:
        return self._collection_name

    def index(
        self,
        embedding_result: EmbeddingResult,
    ):

        ids = []
        documents = []
        embeddings = []
        metadatas = []

        for chunk in embedding_result.embedded_chunks:

            ids.append(
                chunk.id
            )

            documents.append(
                chunk.content
            )

            embeddings.append(
                chunk.embedding
            )

            metadata = dict(
                chunk.metadata
            )

            metadata["parent_id"] = chunk.parent_id

            metadatas.append(
                metadata
            )

        self.collection.upsert(

            ids=ids,

            documents=documents,

            embeddings=embeddings,

            metadatas=metadatas,

        )

        print(
            f"[CHROMA] Indexed {len(ids)} vectors "
            f"into '{self.collection_name}'"
        )

    def similarity_search(
        self,
        query_embedding: list[float],
        k: int = 5,
    ):

        results = self.collection.query(

            query_embeddings=[
                query_embedding
            ],

            n_results=k,

        )

        return results

    def delete_collection(
        self,
    ):

        self.client.delete_collection(
            self.collection_name
        )

        print(
            f"[CHROMA] Deleted collection "
            f"'{self.collection_name}'"
        )

    def reset(
        self,
    ):

        self.delete_collection()

        self.collection = self.client.get_or_create_collection(
            name=self.collection_name
        )

        print(
            f"[CHROMA] Recreated collection "
            f"'{self.collection_name}'"
        )