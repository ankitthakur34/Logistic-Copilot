from app.rag.evaluation.runners.testcase_builder import (
    TestCaseBuilder,
)

from app.rag.evaluation.dataset.dataset_loader import (
    DatasetLoader,
)

dataset = DatasetLoader.load(

    "app/rag/evaluation/dataset/golden_dataset.json"

)

sample = dataset[0]

test_case = TestCaseBuilder.build(

    question=sample["question"],

    expected_answer=sample["expected_answer"],

    actual_answer="Shipment delayed because of power interruption.",

    retrieval=type(
        "obj",
        (),
        {
            "parents": [
                type(
                    "obj",
                    (),
                    {
                        "content":
                        "Shipment delayed because of power interruption."
                    }
                )
            ]
        }
    )()

)

print(test_case)