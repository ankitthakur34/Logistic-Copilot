import json

from app.rag.metadata.base_metadata_extractor import (
    BaseMetadataExtractor,
)

from app.rag.metadata.metadata_result import (
    MetadataResult,
)

from app.rag.prompts.prompt_result import (
    PromptResult,
)

from app.rag.metadata.prompts.metadata_extraction_prompt import build_system_prompt
from app.rag.utils.json_parser import (
    JsonParser,
)


class LLMMetadataExtractor(BaseMetadataExtractor):

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

            system_prompt=build_system_prompt(schema),

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

        return MetadataResult(

            shipment=data.get("shipment"),

            email_id=data.get("email_id"),

            customer=data.get("customer"),

            port=data.get("port"),

            vessel=data.get("vessel"),

            date=data.get("date"),

            priority=data.get("priority"),

            document_type=data.get("document_type"),

        )