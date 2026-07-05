import os

from groq import Groq

from app.rag.llm.base_llm import BaseLLM
from app.rag.llm.llm_result import LLMResult
from app.rag.prompts.prompt_result import PromptResult


class GroqLLM(BaseLLM):

    def __init__(

        self,

        model: str = "llama-3.3-70b-versatile",

    ):

        self.model = model

        self.client = Groq(

            api_key=os.environ["GROQ_API_KEY"]

        )

    def generate(

        self,

        prompt: PromptResult,

    ) -> LLMResult:

        response = self.client.chat.completions.create(

            model=self.model,

            messages=[

                {

                    "role": "system",

                    "content": prompt.system_prompt,

                },

                {

                    "role": "user",

                    "content": prompt.user_prompt,

                },

            ],

            temperature=0,

        )

        return LLMResult(

            answer=response.choices[0].message.content,

            model=response.model,

            usage=response.usage.model_dump()

            if response.usage

            else None,

        )