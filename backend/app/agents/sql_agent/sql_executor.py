from sqlalchemy import text

from app.database.db import db


class SQLExecutor:

    def execute(
        self,
        sql: str,
    ):

        result = db.session.execute(
            text(sql)
        )

        rows = result.fetchall()

        columns = result.keys()

        data = []

        for row in rows:

            data.append(

                dict(

                    zip(
                        columns,
                        row,
                    )

                )

            )

        return data