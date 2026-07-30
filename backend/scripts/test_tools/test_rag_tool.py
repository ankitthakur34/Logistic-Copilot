

from app.bootstrap.service_registry import (
    ServiceRegistry,
)

###############################################################################
# Registry
###############################################################################

registry = ServiceRegistry()

tool = registry.rag_tool

###############################################################################
# Question
###############################################################################

question = "What is the revised ETA of SHP0001?"

###############################################################################
# Execute
###############################################################################

result = tool.execute(

    question=question,

)

###############################################################################
# Print
###############################################################################

print()
print("=" * 80)
print("QUESTION")
print("=" * 80)

print(question)

print()
print("=" * 80)
print("SUCCESS")
print("=" * 80)

print(result.success)

print()
print("=" * 80)
print("ANSWER")
print("=" * 80)

print(result.answer)

print()
print("=" * 80)
print("METADATA")
print("=" * 80)

for key, value in result.metadata.items():

    print(f"{key}: {value}")

print()
print("=" * 80)
print("PARENTS")
print("=" * 80)

retrieval = result.data

for parent in retrieval.parents:

    print(parent.id)
    print(parent.metadata.get("source"))
    print(parent.content[:300])
    print()