import re


class SQLValidator:

    FORBIDDEN = [

        "DELETE",

        "UPDATE",

        "INSERT",

        "DROP",

        "ALTER",

        "TRUNCATE",

        "CREATE",

        "GRANT",

        "REVOKE",
    ]

    def validate(
        self,
        sql: str,
    ):

        sql_upper = sql.upper()

        #
        # only select allowed
        #

        if not sql_upper.startswith(
            "SELECT"
        ):

            raise Exception(
                "Only SELECT statements allowed."
            )

        #
        # dangerous keywords
        #

        for keyword in self.FORBIDDEN:

            if re.search(

                rf"\b{keyword}\b",

                sql_upper,

            ):

                raise Exception(

                    f"Forbidden SQL detected: {keyword}"

                )

        return True