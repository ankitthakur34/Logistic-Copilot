from abc import ABC, abstractmethod

from app.rag.prompts.prompt_result import PromptResult
from app.rag.llm.llm_result import LLMResult


class BaseLLM(ABC):

    @abstractmethod
    def generate(
        self,
        prompt: PromptResult,
    ) -> LLMResult:
        pass