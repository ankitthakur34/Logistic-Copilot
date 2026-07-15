import re


class SQLNormalizer:

    ENUM_VALUES = {

        "priority": {
            "high": "HIGH",
            "medium": "MEDIUM",
            "low": "LOW",
        }

    }

    @classmethod
    def normalize(

        cls,

        sql: str,

    ):

        for field, values in cls.ENUM_VALUES.items():

            for wrong, correct in values.items():

                sql = re.sub(

                    rf"{field}\s*=\s*'{wrong}'",

                    f"{field} = '{correct}'",

                    sql,

                    flags=re.IGNORECASE,

                )

        return sql