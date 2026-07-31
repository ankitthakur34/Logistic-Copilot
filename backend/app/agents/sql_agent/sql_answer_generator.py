from app.rag.prompts.prompt_result import (
    PromptResult,
)

from app.agents.sql_agent.sql_answer_prompt import (
    SQL_ANSWER_SYSTEM_PROMPT,
)


class SQLAnswerGenerator:

    def __init__(
        self,
        llm,
    ):

        self.llm = llm

    def generate(

        self,

        question: str,

        sql: str,

        rows: list[dict],

    ):

        prompt = f"""
QUESTION:

{question}


SQL:

{sql}


RESULTS:

{rows}


Answer ONLY using the database rows.

If the database rows do not contain enough information to answer the user's question,
explicitly state that the information is not available in the database.

Do NOT guess.

Do NOT infer.

Do NOT use outside knowledge.
"""

        result = PromptResult(

            system_prompt=SQL_ANSWER_SYSTEM_PROMPT,

            user_prompt=prompt,

            full_prompt="",
        )

        response = self.llm.generate(
            result
        )

        return response.answer