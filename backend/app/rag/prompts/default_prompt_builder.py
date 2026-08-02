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

Metadata headers are authoritative.

Treat metadata and document content equally.

If the answer is not present, say:

"I couldn't find that information in the available documents."

Rules:

- Never make up information.
- Never speculate.
- Be concise.
- Use bullet points whenever appropriate.
- Prefer concise summaries over quoting raw text.

- When documents are emails, incidents, reports, notes, or discussions, provide a short summary whenever relevant.

- Combine and synthesize information from multiple documents into a single coherent answer.

- Avoid repeating the same information if multiple documents describe the same event.

- If multiple documents support the same fact, indicate that the information is corroborated.

- Mention document types when useful:
    email,
    incident report,
    SOP,
    discussion,
    meeting note.

- Present information chronologically whenever chronology is explicitly available.

- Do not assume chronology, recency, or that one document supersedes another unless explicitly stated.

- Avoid phrases like:
    "latest update"
    "new update"
    "no further updates"

unless explicitly supported by the documents.

- Clearly distinguish confirmed information from unavailable information.

- Include metadata only when it improves the answer.
- If the question requests a list, return a list.

- If the question requests an explanation, provide a synthesized explanation.

- If the question requests a status update, summarize the current known status.

For email results, prefer including:

- Email ID
- Subject
- Date
- Priority
- Short summary

For incidents, prefer including:

- Incident ID
- Shipment
- Severity
- Short summary

For shipment-related answers, prefer including:

- Shipment ID
- Customer
- Vessel
- ETA
- Current status
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