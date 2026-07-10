from app.rag.evaluation.dataset.dataset_loader import (
    DatasetLoader,
)


dataset = DatasetLoader.load(

    "app/rag/evaluation/dataset/golden_dataset.json"

)

for item in dataset:

    print()

    print("=" * 80)

    print(item["question"])

    print(item["expected_answer"])

    print(item["expected_sources"])