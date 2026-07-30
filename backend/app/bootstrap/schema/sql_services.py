from dataclasses import dataclass

from app.agents.sql_agent.sql_agent import SQLAgent


@dataclass
class SQLServices:

    agent: SQLAgent