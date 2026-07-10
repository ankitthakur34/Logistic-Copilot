from app.rag.context.base_context_builder import (
    BaseContextBuilder,
)

from app.rag.context.context_result import (
    ContextResult,
)

from app.rag.schema.retrieval_result import (
    RetrievalResult,
)

from app.rag.context.context_config import (
    NON_CONTEXT_FIELDS,
)


class DefaultContextBuilder(
    BaseContextBuilder
):

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

            source = metadata.get(
                "source"
            )

            if source:

                sources.append(
                    source
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

        for key, value in metadata.items():

            #
            # Ignore internal metadata
            #

            if key.lower() in NON_CONTEXT_FIELDS:

                continue

            if value is None:

                continue

            #
            # Lists
            #

            if isinstance(
                value,
                list,
            ):

                value = ", ".join(
                    str(v)
                    for v in value
                )

            label = (

                key.replace(
                    "_",
                    " ",
                )
                .title()
            )

            lines.append(

                f"{label:<20}: {value}"

            )

        lines.append(
            "=" * 60
        )

        return "\n".join(
            lines
        )