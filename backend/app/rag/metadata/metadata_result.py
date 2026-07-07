from dataclasses import dataclass


@dataclass
class MetadataResult:

    shipment: str | None = None

    email: str | None = None

    customer: str | None = None

    port: str | None = None

    vessel: str | None = None

    date: str | None = None