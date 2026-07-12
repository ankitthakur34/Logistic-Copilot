import json

from app.rag.prompts.prompt_result import PromptResult

from app.rag.evaluation.dataset.generated.generated_question import (
    GeneratedQuestion,
)
from app.rag.utils.json_parser import (
    JsonParser,
)

class QuestionAnswerGenerator:

    def __init__(

        self,

        llm,

    ):

        self.llm = llm

    def generate(

    self,

    parents,

):

    ##################################################
    # Merge contexts
    ##################################################

        contexts = []

        sources = []

        for parent in parents:

            source = parent.metadata.get(

            "source",

            "Unknown",

        )

            sources.append(

            source,

        )

            contexts.append(

f"""
SOURCE:
{source}

CONTENT:
{parent.content}
"""
        )

        merged_context = "\n\n".join(

        contexts,

    )

    ##################################################
    # Prompt
    ##################################################

        user_prompt = f"""
You are creating evaluation datasets for RAG systems.

Below are related documents.

Generate 3 diverse question-answer pairs.

Rules:

1. Prefer questions requiring information from MULTIPLE documents.

2. Questions should resemble real user questions.

3. Avoid trivial metadata questions.

4. Prefer:
    - status questions
    - update questions
    - cause/effect questions
    - summary questions
    - timeline questions

5. Answers must only use provided information.

6. Return ONLY JSON.

Documents:

{merged_context}

Output format:

[
    {{
        "question": "...",
        "answer": "..."
    }}
]
"""

        prompt = PromptResult(

        system_prompt="""
You are an expert synthetic dataset generator.

Return ONLY valid JSON.
""",

        user_prompt=user_prompt,

        full_prompt="",

    )

        response = self.llm.generate(

        prompt,

    )

    ##################################################
    # Parse
    ##################################################

        try:

            data = JsonParser.parse(

    response.answer,

)
            print("DATA")
            print(data)

        except Exception as e:

            print()
            print("=" * 100)
            print("FAILED JSON")
            print("=" * 100)
            print(type(e))
            

            print(

            response.answer,

        )
            

            return []

    ##################################################
    # Build Questions
    ##################################################

        results = []

        for item in data:

            results.append(

            GeneratedQuestion(

                question=item[

                    "question"

                ],

                expected_answer=item[

                    "answer"

                ],

                expected_sources=sources,

            )

        )

        return results