from app.rag.prompts.prompt_result import (
    PromptResult,
)


def build_prompt(

    document,

):

    system_prompt = """
You are an evaluation dataset generator.

Generate:

1 factual question
1 reasoning question
1 summary question.

Return ONLY valid JSON.

Format:

[
    {
        "question": "...",
        "answer": "..."
    }
]
""".strip()

    user_prompt = f"""
DOCUMENT

{document}
""".strip()

    return PromptResult(

        system_prompt=system_prompt,

        user_prompt=user_prompt,

        full_prompt="",

    )