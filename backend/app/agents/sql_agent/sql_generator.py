from app.rag.prompts.prompt_result import (
    PromptResult,
)

from app.agents.sql_agent.sql_prompt import (
    SQL_SYSTEM_PROMPT,
    SQLPromptBuilder,
)


class SQLGenerator:

    def __init__(
        self,
        llm,
    ):

        self.llm = llm

        self.builder = (
            SQLPromptBuilder()
        )

    def generate(
        self,
        question,
        schema,
    ):

        user_prompt = (
            self.builder.build(
                question,
                schema,
            )
        )

        prompt = PromptResult(
            system_prompt=SQL_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            full_prompt=""
        )

        response = (
            self.llm.generate(
                prompt
            )
        )

        sql = (
            response.answer
            .strip()
        )

        sql = (
            sql
            .replace(
                "```sql",
                "",
            )
            .replace(
                "```",
                "",
            )
            .strip()
        )

        return sql