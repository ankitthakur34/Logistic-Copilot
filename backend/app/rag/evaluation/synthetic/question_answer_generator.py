import json

from evaluation.synthetic.question_generation_prompt import (

    build_prompt,

)
from app.rag.utils.json_parser import (
    JsonParser,
)





class QuestionAnswerGenerator:

    def __init__(

        self,

        llm,

    ):

        self.llm = llm

    def generate(

        self,

        parent_chunk,

    ):

        prompt = build_prompt(

            parent_chunk.content,

        )

        response = self.llm.generate(

            prompt,

        )

        try:

            data = JsonParser.parse(

                response.answer,

            )

            return data

        except Exception:

            return []