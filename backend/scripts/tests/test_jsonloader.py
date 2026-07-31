from app.rag.loader.json_loader import (
    JsonLoader,
)


loader = JsonLoader(

    root_path="data/json",

)

documents = loader.load()


print()
print("=" * 100)
print("TOTAL DOCUMENTS")
print("=" * 100)

print(

    len(documents)

)


for i, doc in enumerate(

    documents

):

    print()

    print("=" * 100)
    print(

        f"DOCUMENT {i+1}"

    )
    print("=" * 100)

    print()

    print("CONTENT")
    print("-" * 80)

    print(

        doc.content

    )

    print()

    print("METADATA")
    print("-" * 80)

    for key, value in (

        doc.metadata.items()

    ):

        print(

            f"{key}: {value}"

        )