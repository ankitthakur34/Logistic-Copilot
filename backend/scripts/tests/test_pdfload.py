from app.rag.loader.pdf_loader import PdfLoader


loader = PdfLoader(

    "data/pdf"

)

docs = loader.load()

for doc in docs:

    print()

    print(

        doc.metadata

    )

    print(

        doc.content[:300]

    )