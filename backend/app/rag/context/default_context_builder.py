from app.rag.context.base_context_builder import (
    BaseContextBuilder,
)

from app.rag.context.context_result import (
    ContextResult,
)

from app.rag.schema.retrieval_result import (
    RetrievalResult,
)


class DefaultContextBuilder(BaseContextBuilder):

    def build(
        self,
        retrieval: RetrievalResult,
    ) -> ContextResult:

        sections = []

        sources = []

        for parent in retrieval.parents:

            metadata = parent.metadata

            header = self._build_header(
                metadata
            )

            sections.append(
                f"""
{header}

{parent.content.strip()}
""".strip()
            )

            sources.append(
                metadata.get(
                    "source",
                    "Unknown",
                )
            )

        context = "\n\n".join(
            sections
        )

        return ContextResult(

            context=context,

            sources=sources,

            document_count=len(
                retrieval.parents
            ),

        )

    def _build_header(
        self,
        metadata: dict,
    ) -> str:

        lines = [
            "=" * 60,
        ]

        field_mapping = [

            ("document_type", "DOCUMENT TYPE"),

            ("shipment", "SHIPMENT"),

            ("customer", "CUSTOMER"),

            ("incident_id", "INCIDENT ID"),

            ("email_id", "EMAIL ID"),

            ("vessel", "VESSEL"),

            ("origin", "ORIGIN"),

            ("destination", "DESTINATION"),

            ("priority", "PRIORITY"),

            ("severity", "SEVERITY"),

            ("category", "CATEGORY"),

            ("date", "DATE"),

            ("folder", "FOLDER"),

            ("source", "SOURCE"),

        ]

        for key, label in field_mapping:

            value = metadata.get(key)

            if value:

                lines.append(
                    f"{label:<15}: {value}"
                )

        lines.append("=" * 60)

        return "\n".join(lines)