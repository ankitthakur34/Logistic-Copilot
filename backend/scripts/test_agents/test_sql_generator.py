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
from app.agents.sql_agent.sql_validator import (
    SQLValidator,
)

from app.agents.sql_agent.sql_generator import (
    SQLGenerator,
)

from app.rag.llm.groq_llm import (
    GroqLLM,
)

app = create_app()

with app.app_context():

    schema = (
        SchemaBuilder()
        .build()
    )

    generator = (
        SQLGenerator(
            llm=GroqLLM()
        )
    )

    question = (
        "Which users own high priority tasks for shipments going to Singapore?"
    )

    sql = generator.generate(
        question,
        schema,
    )

    print()

    print("="*80)
    print("QUESTION")
    print(question)

    print()
    print("="*80)
    print("SQL")
    print(sql)