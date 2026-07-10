from deepeval.metrics import (

    FaithfulnessMetric,

    AnswerRelevancyMetric,

    ContextualPrecisionMetric,

    ContextualRecallMetric,

)

from app.rag.evaluation.models.groq_deepeval_llm import GroqDeepEvalLLM





def build_metrics():

    evaluator = (

        GroqDeepEvalLLM()

    )

    return [

        FaithfulnessMetric(

            threshold=0.7,
            model=evaluator,

        ),

        AnswerRelevancyMetric(

            threshold=0.7,
            model=evaluator,

        ),

        ContextualPrecisionMetric(

            threshold=0.7,
            model=evaluator,

        ),

        ContextualRecallMetric(

            threshold=0.7,
            model=evaluator,

        ),

    ]