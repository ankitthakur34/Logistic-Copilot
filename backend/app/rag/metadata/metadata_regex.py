import re

PATTERNS = {

    # Logistics
    "shipment_id": re.compile(r"\bSHP\d{4}\b", re.IGNORECASE),
    "email_id": re.compile(r"\bEMAIL-\d+\b", re.IGNORECASE),
    "incident_id": re.compile(r"\bINC\d+\b", re.IGNORECASE),

    # Generic IDs
    "invoice_id": re.compile(r"\bINV-\d+\b", re.IGNORECASE),
    "container_id": re.compile(r"\b[A-Z]{4}\d{7}\b"),

    # Generic
    "date": re.compile(r"\b\d{4}-\d{2}-\d{2}\b"),
}