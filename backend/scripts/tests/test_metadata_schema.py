# from app.rag.metadata.metadata_schema_builder import (
#     MetadataSchemaBuilder,
# )

# from app.rag.ingestion.ingest_pipeline import (
#     IngestionPipeline,
# )

# ingestion = IngestionPipeline(

#     loader=MultiLoader(

#     loaders=[

#         MarkdownLoader(
#             "data/rag"
#         ),
#         PdfLoader(
#             "data/pdf"
#         ),
#         CsvLoader(
#             "data/csv"
#         ),
#         JsonLoader(
#             "data/json"
#         )

#     ]

# ),

#     chunker=ParentChildChunker(),

# ).run()

# ingestion = pipeline.run()

# schema = (

#     MetadataSchemaBuilder()

#     .build(

#         ingestion.parent_chunks
#     )

# )

# print()

# print(schema.queryable_fields)