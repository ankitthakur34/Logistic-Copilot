import json

from app.rag.evaluation.dataset.evaluation_sample import (
    EvaluationSample,
)


class EvaluationDatasetLoader:

    def load(

        self,

        path: str,

    ):

        with open(

            path,

            "r",

            encoding="utf-8",

        ) as f:

            data = json.load(f)

        samples = []

        for item in data:

            samples.append(

                EvaluationSample(

                    question=item.get(

                        "question",

                        "",

                    ),

                    expected_answer=item.get(

                        "expected_answer",

                        "",

                    ),

                    expected_sources=item.get(

                        "expected_sources",

                        [],

                    ),

                )

            )

        return samples