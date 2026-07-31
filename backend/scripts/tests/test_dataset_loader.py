from app.rag.evaluation.dataset.evaluation_dataset_loader import (
    EvaluationDatasetLoader,
)

loader = EvaluationDatasetLoader()

dataset = loader.load(

    "app/rag/evaluation/dataset/generated/generated_dataset.json",

)

print()

print("=" * 80)
print("DATASET")
print("=" * 80)

for sample in dataset[:5]:

    print()

    print(sample)