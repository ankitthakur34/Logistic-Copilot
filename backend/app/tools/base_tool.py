from abc import ABC
from abc import abstractmethod

from app.tools.tool_result import (
    ToolResult,
)


class BaseTool(ABC):

    #
    # Human readable name
    #

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    #
    # Used by Router LLM
    #

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    #
    # Execute tool
    #

    @abstractmethod
    def execute(
    self,
    **kwargs,
) -> ToolResult:

        pass