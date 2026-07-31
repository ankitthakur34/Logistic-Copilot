from dataclasses import dataclass
from typing import List

from app.agents.router_agent.router_decision import (
    RouterDecision,
)


@dataclass
class RouterResult:

    #################################################
    # Selected Tools
    #################################################

    tools: List[RouterDecision]

    #################################################
    # Confidence
    #################################################

    confidence: float

    #################################################
    # Reason
    #################################################

    reason: str