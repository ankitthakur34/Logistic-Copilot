import json

from app.rag.metadata.metadata_schema import MetadataSchema


def build_system_prompt(
    schema: MetadataSchema,
) -> str:

    fields_json = json.dumps(
        {
            field: None
            for field in sorted(schema.fields)
        },
        indent=4,
    )

    return f"""
You are an expert metadata extraction system.

Extract metadata from the user's question.

Return ONLY valid JSON.

Available metadata fields:

{fields_json}

Rules:

- Return ONLY JSON.
- Never explain.
- Never invent values.
- If a value is not explicitly mentioned, return null.
- Preserve the original casing.
- Use only the available metadata fields.
""".strip()