import chromadb


client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = (

    client.get_collection(
        "cargo_ai"
    )
)


result = collection.get(

    where={
        "shipment_id":
        "SHP0102"
    },

    include=[
        "metadatas"
    ]
)

print()

print(result)