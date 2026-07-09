from opentelemetry import context

from app.rag.context.default_context_builder import (
    DefaultContextBuilder,
)
from app.rag.prompts.base_prompt_builder import BasePromptBuilder
from app.rag.prompts.prompt_result import PromptResult
from app.rag.schema.retrieval_result import RetrievalResult


class DefaultPromptBuilder(BasePromptBuilder):

    SYSTEM_PROMPT = """
You are an AI assistant.

Answer ONLY using the provided context.

Rules:

- Never make up information.

- Metadata headers are authoritative.

- Treat metadata and document content equally.

- If the answer is not present say:

"I couldn't find that information in the available documents."

- Be concise.

- Use bullet points whenever appropriate.

- Combine information from multiple documents whenever possible.
""".strip()

    def __init__(self):

        self.context_builder = (

        DefaultContextBuilder()

    )

    def build(
        self,
        question: str,
        retrieval: RetrievalResult,
    ) -> PromptResult:

        context = (

    self.context_builder
    .build(
        retrieval,
    )
    .context

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
        print()
        print("=" * 80)
        print("CONTEXT fULL PROPMT")
        print("=" * 80)
        print(full_prompt)
        print()

        return PromptResult(

            system_prompt=self.SYSTEM_PROMPT,

            user_prompt=user_prompt,

            full_prompt=full_prompt,

        )