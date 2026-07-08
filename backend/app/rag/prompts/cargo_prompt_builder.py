from app.rag.context.context_formatter import ContextFormatter

from app.rag.prompts.base_prompt_builder import BasePromptBuilder
from app.rag.prompts.prompt_result import PromptResult
from app.rag.schema.retrieval_result import RetrievalResult


class CargoPromptBuilder(BasePromptBuilder):

    SYSTEM_PROMPT = """
You are CargoAI.

You are an expert logistics and shipping assistant.

Answer ONLY using the provided context.

Rules:

- Never make up information.

- If the answer is not present say:

"I couldn't find that information in the available documents."

- Be concise.

- Use bullet points whenever appropriate.

- Mention shipment IDs whenever available.

- Mention ports, incidents and SOPs whenever relevant.

- If multiple documents support the answer,
combine them into a single answer.
""".strip()

    def __init__(self):

        self.context_formatter = ContextFormatter()

    def build(
        self,
        question: str,
        retrieval: RetrievalResult,
    ) -> PromptResult:

        context = self.context_formatter.format(
            retrieval,
        )

        user_prompt = f"""
CONTEXT

{context}

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