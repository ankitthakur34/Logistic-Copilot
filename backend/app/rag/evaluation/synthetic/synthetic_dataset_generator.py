import json
from pathlib import Path

from app.rag.evaluation.dataset.generated.generated_question import GeneratedQuestion




class SyntheticDatasetGenerator:

    def __init__(

        self,

        qa_generator,

    ):

        self.qa_generator = qa_generator

    def generate(

        self,

        ingestion,

    ):

        dataset = []

        for parent in ingestion.parent_chunks:

            qa_pairs = (

                self.qa_generator.generate(

                    parent,

                )
            )

            for qa in qa_pairs:

                dataset.append(

                    GeneratedQuestion(

                        question=qa["question"],

                        expected_answer=qa["answer"],

                        expected_sources=[

    parent.metadata.get(

        "source",

        "Unknown"

    )
]

                    )

                )

        return dataset

    def save(

        self,

        dataset,

        path,

    ):

        data = []

        for item in dataset:

            data.append(

                {

                    "question":
                        item.question,

                    "expected_answer":
                        item.expected_answer,

                    "expected_sources":
                        item.expected_sources,

                }

            )

        Path(path).parent.mkdir(

            parents=True,

            exist_ok=True,

        )

        with open(

            path,

            "w",

            encoding="utf-8",

        ) as f:

            json.dump(

                data,

                f,

                indent=4,

                ensure_ascii=False,

            )