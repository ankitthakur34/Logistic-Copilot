from app.rag.metadata.regex_metadata_extractor import (
    RegexMetadataExtractor,
)


extractor = RegexMetadataExtractor()


questions = [

    "Why is shipment SHP0007 delayed?",

    "Show EMAIL-005",

    "Status of SHP0010",

    "Tell me about shipment shp0004",

    "General shipping process",

]


for question in questions:

    print("=" * 80)

    print(question)

    print()

    result = extractor.extract(
        question,
    )

    print(result)