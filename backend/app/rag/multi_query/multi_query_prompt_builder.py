from app.rag.prompts.prompt_result import PromptResult

from app.rag.multi_query.prompt import SYSTEM_PROMPT


class MultiQueryPromptBuilder:

    def build(
        self,
        question: str,
    ) -> PromptResult:

        return PromptResult(

            system_prompt=SYSTEM_PROMPT,

            user_prompt=question,

            full_prompt=None,

        )