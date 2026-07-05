from dataclasses import dataclass


@dataclass
class PromptResult:

    system_prompt: str

    user_prompt: str

    full_prompt: str