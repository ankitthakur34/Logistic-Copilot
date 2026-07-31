from app.agents.router_agent.router_parser import (
    RouterParser,
)

response = """
{
    "tools":[
        "sql",
        "rag"
    ],
    "confidence":0.95,
    "reason":"Need shipment metadata and incident documents."
}
"""

result = RouterParser.parse(

    response

)

print(result)