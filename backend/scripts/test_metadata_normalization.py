from app.rag.loader.markdown_loader import (
    MarkdownLoader,
)

from app.rag.loader.json_loader import (
    JsonLoader,
)

from app.rag.loader.csv_loader import (
    CsvLoader,
)

from app.rag.loader.pdf_loader import (
    PdfLoader,
)


loaders = [

    MarkdownLoader(
        "data/rag"
    ),

    JsonLoader(
        "data/json"
    ),

    CsvLoader(
        "data/csv"
    ),

    PdfLoader(
        "data/pdf"
    ),
]


for loader in loaders:

    print()
    print("=" * 100)
    print(loader.__class__.__name__)
    print("=" * 100)

    docs = loader.load()

    for doc in docs[:3]:

        print()

        print(doc.metadata)