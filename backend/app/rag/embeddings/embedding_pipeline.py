from app.rag.embeddings.base_embedding import BaseEmbedding


class EmbeddingPipeline:

    def __init__(
        self,
        embedding_model: BaseEmbedding,
    ):
        self.embedding_model = embedding_model

    def run(
        self,
        child_chunks,
    ):

        texts = [
            chunk.content
            for chunk in child_chunks
        ]

        embeddings = self.embedding_model.embed_documents(
            texts
        )

        return embeddings