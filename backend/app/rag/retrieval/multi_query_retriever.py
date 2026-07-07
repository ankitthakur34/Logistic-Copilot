from app.rag.retrieval.base_retriever import BaseRetriever
from app.rag.schema.search_result import SearchResult


class MultiQueryRetriever(BaseRetriever):

    def __init__(
        self,
        embedding_model,
        generator,
        retriever,
        fusion,
    ):
        self.embedding_model = embedding_model
        self.generator = generator
        self.retriever = retriever
        self.fusion = fusion

    def retrieve(
        self,
        query_embedding=None,
        question=None,
        where=None,
        top_k=5,
    ) -> SearchResult:

        queries = self.generator.generate(question)

        if question not in queries:
            queries.insert(0, question)

        search_results = []

        for query in queries:

            embedding = self.embedding_model.embed_query(
                query,
            )

            result = self.retriever.retrieve(
                query_embedding=embedding,
                question=query,
                where=where,
                top_k=top_k,
            )

            search_results.append(result)

        return self.fusion.fuse(search_results)