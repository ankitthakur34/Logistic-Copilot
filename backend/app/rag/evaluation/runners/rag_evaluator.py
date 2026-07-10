from deepeval.evaluate import evaluate

from evaluation.runners.testcase_builder import (
    TestCaseBuilder,
)


class RAGEvaluator:

    def __init__(

        self,

        metrics,

    ):

        self.metrics = metrics

    def evaluate_question(

        self,

        question,

        expected_answer,

        actual_answer,

        retrieval,

    ):

        test_case = (

            TestCaseBuilder.build(

                question=question,

                expected_answer=expected_answer,

                actual_answer=actual_answer,

                retrieval=retrieval,

            )

        )

        result = evaluate(

            test_cases=[

                test_case

            ],

            metrics=self.metrics,

        )

        return result