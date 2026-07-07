from app.rag.multi_query.base_multi_query_generator import (
    BaseMultiQueryGenerator,
)


class MultiQueryPipeline:

    def __init__(
        self,
        generator: BaseMultiQueryGenerator,
    ):

        self.generator = generator

    def run(
        self,
        question: str,
    ) -> list[str]:

        queries = self.generator.generate(
            question
        )

        queries.insert(
            0,
            question,
        )

        unique_queries = []

        seen = set()

        for query in queries:

            key = query.lower().strip()

            if key not in seen:

                seen.add(key)

                unique_queries.append(query)

        return unique_queries