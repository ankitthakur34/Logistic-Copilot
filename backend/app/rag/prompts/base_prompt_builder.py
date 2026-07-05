from abc import ABC, abstractmethod

from app.rag.context.context_result import ContextResult
from app.rag.prompts.prompt_result import PromptResult


class BasePromptBuilder(ABC):

    @abstractmethod
    def build(
        self,
        question: str,
        context: ContextResult,
    ) -> PromptResult:
        pass