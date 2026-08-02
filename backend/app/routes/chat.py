from flask import Blueprint
from flask import request
from flask import jsonify

from app.bootstrap.service_registry import ServiceRegistry

chat_bp = Blueprint(
    "chat",
    __name__,
)

registry = ServiceRegistry()


@chat_bp.post("/chat")
def chat():

    question = request.json["question"]

    state = registry.graph.invoke(
        {
            "question": question,
        }
    )

    execution = state["execution_result"]

    return jsonify(
        {
            "answer": execution.answer,
            "tool_results": [
                {
                    "tool_name": tool.tool_name,
                    "success": tool.success,
                    "sources": tool.sources,
                }
                for tool in execution.tool_results
            ],
        }
    )