from deepeval.models.base_model import (
    DeepEvalBaseLLM,
)

from groq import Groq

import os


class GroqDeepEvalLLM(

    DeepEvalBaseLLM,

):

    def __init__(

        self,

        model="llama-3.3-70b-versatile",

    ):

        self.model = model

        self.client = Groq(

            api_key=os.getenv(

                "GROQ_API_KEY"

            )

        )

    def load_model(self):

        return self.client

    def generate(

        self,

        prompt: str,

    ) -> str:

        response = self.client.chat.completions.create(

            model=self.model,

            messages=[

                {

                    "role": "user",

                    "content": prompt,

                }

            ],

            temperature=0,

        )

        return (

            response

            .choices[0]

            .message.content

        )

    async def a_generate(

        self,

        prompt: str,

    ):

        return self.generate(prompt)

    def get_model_name(

        self,

    ):

        return self.model