from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolResult:

    #
    # Which tool generated this response
    #
    tool_name: str

    #
    # Whether execution succeeded
    #
    success: bool

    #
    # Natural language answer
    #
    answer: str

    #
    # Raw structured output
    #
    data: Any = None

    #
    # Additional metadata
    #
    metadata: dict = field(default_factory=dict)

    #
    # Sources used
    #
    sources: list = field(default_factory=list)

    #
    # Error (if any)
    #
    error: str | None = None