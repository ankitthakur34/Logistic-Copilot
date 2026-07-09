from app.rag.metadata.base_metadata_extractor import (
    BaseMetadataExtractor,
)

from app.rag.metadata.metadata_result import (
    MetadataResult,
)

from app.rag.prompts.prompt_result import (
    PromptResult,
)

from app.rag.metadata.prompts.metadata_extraction_prompt import (
    build_system_prompt,
)

from app.rag.utils.json_parser import (
    JsonParser,
)


class LLMMetadataExtractor(
    BaseMetadataExtractor,
):

    def __init__(

        self,

        llm,

    ):

        self.llm = llm

    def extract(

        self,

        question: str,

        schema,

    ) -> MetadataResult:

        prompt = PromptResult(

            system_prompt=build_system_prompt(
                schema,
            ),

            user_prompt=question,

            full_prompt="",

        )

        response = self.llm.generate(

            prompt,

        )

        try:

            data = JsonParser.parse(

                response.answer,

            )

        except Exception:

            return MetadataResult()

        metadata = MetadataResult()

        #
        # Dynamically store fields
        #

        for field, value in data.items():

            if value is None:

                continue

            metadata.set(

                field,

                value,

            )

        return metadata