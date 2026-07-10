import json

from pathlib import Path

from datetime import datetime


class ReportWriter:

    REPORT_DIR = (

        Path(

            "app/rag/evaluation/reports"

        )

    )

    @classmethod
    def save(

        cls,

        report,

    ):

        cls.REPORT_DIR.mkdir(

            parents=True,

            exist_ok=True,

        )

        timestamp = (

            datetime.now()

            .strftime(

                "%Y_%m_%d_%H_%M_%S"

            )

        )

        path = (

            cls.REPORT_DIR

            /

            f"evaluation_{timestamp}.json"

        )

        with open(

            path,

            "w",

            encoding="utf8",

        ) as f:

            json.dump(

                report,

                f,

                indent=4,

                ensure_ascii=False,

            )

        print()

        print(

            "Saved report:",

            path,

        )

        return path