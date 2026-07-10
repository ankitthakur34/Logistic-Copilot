class DecompositionPipeline:

    def __init__(

        self,

        decomposer,

    ):

        self.decomposer = decomposer

    def run(

        self,

        question: str,

    ) -> list[str]:

        queries = self.decomposer.decompose(
            question
        )

        #
        # Deduplicate
        #

        unique = []

        seen = set()

        for query in queries:

            key = query.lower().strip()

            if key in seen:

                continue

            seen.add(
                key
            )

            unique.append(
                query
            )

        return unique