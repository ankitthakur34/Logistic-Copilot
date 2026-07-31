from app.rag.loader.csv_loader import (
    CsvLoader,
)


loader = CsvLoader(

    root_path="data/csv",

)

documents = loader.load()


print()
print("=" * 100)
print("TOTAL DOCUMENTS")
print("=" * 100)

print(

    len(documents)

)


for idx, doc in enumerate(documents):

    print()

    print("=" * 100)
    print(f"DOCUMENT {idx + 1}")
    print("=" * 100)

    print()

    print("CONTENT")
    print("-" * 80)

    print(doc.content)

    print()

    print("METADATA")
    print("-" * 80)

    for key, value in doc.metadata.items():

        print(

            f"{key}: {value}"

        )