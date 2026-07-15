import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

sys.path.append(
    str(ROOT)
)


from app import create_app

from app.agents.sql_agent.sql_executor import (
    SQLExecutor,
)

app = create_app()

with app.app_context():

    sql = """
    SELECT u.name FROM users u JOIN tasks t ON u.id = t.owner_id JOIN shipments s ON t.shipment_id = s.id WHERE s.shipment_no = 'SHP0001' LIMIT 100
    """

    result = (
        SQLExecutor()
        .execute(sql)
    )

    print(result)