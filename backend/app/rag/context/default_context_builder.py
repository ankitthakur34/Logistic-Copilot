from app.rag.context.base_context_builder import (
    BaseContextBuilder,
)

from app.rag.context.context_result import (
    ContextResult,
)

from app.rag.schema.retrieval_result import (
    RetrievalResult,
)


class DefaultContextBuilder(
    BaseContextBuilder,
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
                metadata,
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
            sections,
        )

        return ContextResult(

            context=context,

            sources=sources,

            document_count=len(
                retrieval.parents,
            ),

        )

    def _build_header(

        self,

        metadata: dict,

    ) -> str:

        lines = [

            "=" * 60,

        ]

        for key, value in sorted(

            metadata.items()

        ):

            if value is None:

                continue

            #
            # Skip dictionaries
            #

            if isinstance(
                value,
                dict,
            ):

                continue

            #
            # Lists
            #

            if isinstance(
                value,
                list,
            ):

                value = ", ".join(

                    map(
                        str,
                        value,
                    )

                )

            label = (

                key
                .replace(
                    "_",
                    " ",
                )
                .title()

            )

            lines.append(

                f"{label:<20}: {value}"

            )

        lines.append(

            "=" * 60,

        )

        print(
            f"Built header for metadata: {metadata}"
        )

        return "\n".join(
            lines,
        )