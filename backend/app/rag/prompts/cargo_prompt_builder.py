from app.rag.context.context_result import ContextResult
from app.rag.prompts.base_prompt_builder import (
    BasePromptBuilder,
)
from app.rag.prompts.prompt_result import (
    PromptResult,
)


class CargoPromptBuilder(BasePromptBuilder):

    SYSTEM_PROMPT = """
You are CargoAI.

You are an expert logistics and shipping assistant.

Answer ONLY using the provided context.

Rules:

- Never make up information.
- If the answer is not present, say:
  "I couldn't find that information in the available documents."

- Be concise.
- Use bullet points whenever appropriate.
- Mention shipment IDs when available.
- Mention ports, incidents, and SOPs whenever relevant.
""".strip()

    def build(
        self,
        question: str,
        context: ContextResult,
    ) -> PromptResult:

        user_prompt = f"""
CONTEXT

{context.context}

------------------------------------------------------------

QUESTION

{question}
""".strip()

        full_prompt = f"""
SYSTEM

{self.SYSTEM_PROMPT}

============================================================

{user_prompt}
""".strip()

        return PromptResult(

            system_prompt=self.SYSTEM_PROMPT,

            user_prompt=user_prompt,

            full_prompt=full_prompt,

        )