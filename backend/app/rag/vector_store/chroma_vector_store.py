
import chromadb
from app.rag.vector_store.base_vector_store import BaseVectorStore
from app.rag.schema.search_result import SearchResult


class ChromaVectorStore(BaseVectorStore):

    def __init__(
        self,
        persist_directory: str = "./chroma_db",
        collection_name: str = "cargo_ai",
    ):

        self.client = chromadb.PersistentClient(
            path=persist_directory
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    # ---------------------------------------------------------
    # Index
    # ---------------------------------------------------------

    def clear(self):

        self.collection.delete(
        where={}
    )

    def index(
    self,
    child_chunks,
    embeddings,
):

        self.collection.upsert(

        ids=[
            chunk.id
            for chunk in child_chunks
        ],

        documents=[
            chunk.content
            for chunk in child_chunks
        ],

        embeddings=embeddings,

        metadatas=[
            {
                **chunk.metadata,
                "parent_id": chunk.parent_id,
            }
            for chunk in child_chunks
        ],
    )

   
         
           

    # ---------------------------------------------------------
    # Search
    # ---------------------------------------------------------

    def search(
    self,
    query_embedding: list[float],
    top_k: int = 5,
    where : dict | None = None,
) -> SearchResult:

        kwargs = {

        "query_embeddings": [query_embedding],

        "n_results": top_k,

    }
        
        print("=" * 80)
        print("WHERE FILTER")
        print(where)
        print("=" * 80)

        if where:

            kwargs["where"] = where

        result = self.collection.query(
        **kwargs,
        )

        return SearchResult(

        ids=result["ids"][0],

        # documents=result["documents"][0],

        # metadatas=result["metadatas"][0],

        scores=result["distances"][0],

    )

    # ---------------------------------------------------------
    # Reset
    # ---------------------------------------------------------

    def reset(self):

        name = self.collection.name

        self.client.delete_collection(name)

        self.collection = self.client.get_or_create_collection(
            name=name
        )

        print(
            f"[CHROMA] Recreated collection '{name}'"
        )

    # ---------------------------------------------------------
    # Count
    # ---------------------------------------------------------

    def count(self):

        return self.collection.count()