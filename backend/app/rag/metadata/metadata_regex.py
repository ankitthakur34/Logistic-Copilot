import re

PATTERNS = {

    "shipment": re.compile(
        r"\bSHP\d{4}\b",
        re.IGNORECASE,
    ),

    "email": re.compile(
        r"\bEMAIL-\d+\b",
        re.IGNORECASE,
    ),

    "date": re.compile(
        r"\b\d{4}-\d{2}-\d{2}\b",
    ),

}