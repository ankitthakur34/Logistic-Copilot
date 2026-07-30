

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

from app.tools.sql_tool import (
    SQLTool,
)

app = create_app()

with app.app_context():

    ###################################################
    # SQL Agent
    ###################################################

    agent = SQLAgent(

        schema_builder=SchemaBuilder(),

        sql_generator=SQLGenerator(

            llm=GroqLLM()

        ),

        validator=SQLValidator(),

        executor=SQLExecutor(),

        answer_generator=SQLAnswerGenerator(

            llm=GroqLLM()

        ),
    )

    ###################################################
    # SQL Tool
    ###################################################

    tool = SQLTool(

        agent=agent,

    )

    ###################################################
    # Test Questions
    ###################################################

    questions = [

        "Show all shipments",

        "Show containers of SHP0001",

        "Who owns tasks for SHP0001?",

        "Which users own high priority tasks for shipments going to Singapore?",

    ]

    ###################################################
    # Run
    ###################################################

    for question in questions:

        print()
        print("=" * 100)
        print(question)
        print("=" * 100)

        result = tool.execute(

            question=question,

        )

        print()
        print("SUCCESS")
        print(result.success)

        print()
        print("ANSWER")
        print(result.answer)

        print()
        print("ROWS")
        print(result.data)

        print()
        print("METADATA")
        print(result.metadata)

        if not result.success:

            print()
            print("ERROR")
            print(result.error)