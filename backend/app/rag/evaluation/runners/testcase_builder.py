from deepeval.test_case import (
    LLMTestCase,
)

class TestCaseBuilder:

    @staticmethod
    def build(

        question,

        expected_answer,

        actual_answer,

        retrieval,

    ):

        context = [

            parent.content

            for parent in retrieval.parents

        ]

        return LLMTestCase(

            input=question,

            actual_output=actual_answer,

            expected_output=expected_answer,

            retrieval_context=context,

        )