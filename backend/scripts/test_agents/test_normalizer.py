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

app = create_app()

with app.app_context():

    schema = (
        SchemaBuilder()
        .build()
    )

from app.agents.sql_agent.sql_normalizer import (
    SQLNormalizer
)

sql = """

SELECT *
FROM tasks
WHERE priority='High'

"""

print(

    SQLNormalizer.normalize(
        sql
    )

)