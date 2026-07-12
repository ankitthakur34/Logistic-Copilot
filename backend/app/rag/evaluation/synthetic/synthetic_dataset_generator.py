import json
from pathlib import Path

from app.rag.evaluation.dataset.generated.generated_question import (
    GeneratedQuestion,
)

from app.rag.evaluation.dataset.document_grouper import (
    DocumentGrouper,
)



class SyntheticDatasetGenerator:

    def __init__(

        self,

        qa_generator,

        document_grouper=None,

    ):

        self.qa_generator = qa_generator

        self.document_grouper = (

            document_grouper

            or

            DocumentGrouper()

        )

    def generate(

        self,

        ingestion,

    ):

        dataset = []

        ####################################################
        # Build document groups
        ####################################################

        groups = (

            self.document_grouper.group(

                ingestion.parent_chunks,

            )

        )
        groups = groups[:10]

        print()
        print("=" * 100)
        print("TOTAL GROUPS")
        print("=" * 100)
        print(len(groups))

        ####################################################
        # Generate QA from every group
        ####################################################

        for idx, group in enumerate(groups):

            print()
            print("=" * 100)
            print(f"GROUP {idx + 1}")
            print("=" * 100)

            sources = []

            for parent in group:

                source = (

                    parent.metadata.get(

                        "source",

                        "Unknown",

                    )

                )

                sources.append(

                    source,

                )

                print(source)

            ################################################
            # Generate QA
            ################################################

            qa_pairs = (

                self.qa_generator.generate(

                    group,

                )

            )

            ################################################
            # Store dataset
            ################################################

            for qa in qa_pairs:

                #
                # generator may already return
                # GeneratedQuestion
                #

                if isinstance(

                    qa,

                    GeneratedQuestion,

                ):

                    dataset.append(

                        qa,

                    )

                    continue

                #
                # old dict format support
                #

                dataset.append(

                    GeneratedQuestion(

                        question=qa[

                            "question"

                        ],

                        expected_answer=qa[

                            "answer"

                        ],

                        expected_sources=sources,

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