

from app import create_app

from app.bootstrap.service_registry import (
    ServiceRegistry,
)

###############################################################################
# Flask
###############################################################################

app = create_app()

###############################################################################
# Run
###############################################################################

with app.app_context():

    registry = ServiceRegistry()

    tool = registry.sql_tool

    question = (

        "Which users own high priority tasks "

        "for shipments going to Singapore?"

    )

    result = tool.execute(

        question=question,

    )

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
    print("ROWS")
    print("=" * 80)

    for row in result.data:

        print(row)

    print()
    print("=" * 80)
    print("METADATA")
    print("=" * 80)

    for key, value in result.metadata.items():

        print(f"{key}: {value}")