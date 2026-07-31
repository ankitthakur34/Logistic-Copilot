from app.rag.prompts.prompt_result import (
    PromptResult,
)

from app.tools.tool_result import (
    ToolResult,
)

ROUTER_MERGER_SYSTEM_PROMPT = """
You are an AI assistant.

You are given outputs from one or more tools.

Combine them into ONE final answer.

Rules:

- Do not mention SQL or RAG.
- Do not mention tools.
- Merge duplicate information.
- Keep the answer concise.
- If one tool failed but another succeeded,
  answer using the successful tool.
- If all tools failed,
  explain that the information could not be found.
"""


class RouterAnswerMerger:

    def __init__(

        self,

        llm,

    ):

        self.llm = llm

    #################################################

    def merge(

        self,

        question: str,

        results: list[ToolResult],

    ):

        successful = [

            r

            for r in results

            if r.success

        ]

        if not successful:

            return "I couldn't find an answer."

        context = ""

        for result in successful:

            context += (

                f"\n"

                f"Tool: {result.tool_name}\n"

                f"Answer:\n"

                f"{result.answer}\n"

            )

        user_prompt = f"""
Question:

{question}


Tool Outputs:

{context}


Generate ONE final answer.
"""

        prompt = PromptResult(

            system_prompt=ROUTER_MERGER_SYSTEM_PROMPT,

            user_prompt=user_prompt,

            full_prompt="",

        )

        response = self.llm.generate(

            prompt

        )

        return response.answer