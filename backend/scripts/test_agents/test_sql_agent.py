import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

sys.path.append(
    str(ROOT)
)

from app import create_app

from app.agents.sql_agent.schema_builder import (
    SchemaBuilder,
)

from app.agents.sql_agent.sql_generator import (
    SQLGenerator,
)

from app.agents.sql_agent.sql_validator import (
    SQLValidator,
)

from app.agents.sql_agent.sql_executor import (
    SQLExecutor,
)

from app.agents.sql_agent.sql_answer_generator import (
    SQLAnswerGenerator,
)

from app.agents.sql_agent.sql_agent import (
    SQLAgent,
)

from app.rag.llm.groq_llm import (
    GroqLLM,
)

app = create_app()

with app.app_context():

    agent = SQLAgent(

        schema_builder=SchemaBuilder(),

        sql_generator=SQLGenerator(

            llm=GroqLLM()

        ),

        validator=SQLValidator(),

        executor=SQLExecutor(),

        answer_generator=(

            SQLAnswerGenerator(

                llm=GroqLLM()

            )

        ),
    )

    question = (

        "Which users own high priority tasks for shipments going to Singapore?"

    )

    result = agent.run(
        question
    )

    print()
    print("=" * 80)
    print("QUESTION")
    print(result.question)

    print()
    print("=" * 80)
    print("SQL")
    print(result.sql)

    print()
    print("=" * 80)
    print("ROWS")
    print(result.rows)

    print()
    print("=" * 80)
    print("ANSWER")
    print(result.answer)