from app.bootstrap.llm import get_llm
from app.bootstrap.schema.sql_services import SQLServices

from app.agents.sql_agent.schema_builder import SchemaBuilder
from app.agents.sql_agent.sql_generator import SQLGenerator
from app.agents.sql_agent.sql_validator import SQLValidator
from app.agents.sql_agent.sql_executor import SQLExecutor
from app.agents.sql_agent.sql_answer_generator import SQLAnswerGenerator
from app.agents.sql_agent.sql_agent import SQLAgent


def build_sql():

    llm = get_llm()

    agent = SQLAgent(

        schema_builder=SchemaBuilder(),

        sql_generator=SQLGenerator(

            llm=llm,

        ),

        validator=SQLValidator(),

        executor=SQLExecutor(),

        answer_generator=SQLAnswerGenerator(

            llm=llm,

        ),

    )

    return SQLServices(

        agent=agent,

    )