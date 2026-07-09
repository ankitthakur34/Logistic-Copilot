from dataclasses import asdict, dataclass


@dataclass
class MetadataResult:

    shipment: str | None = None

    email_id: str | None = None

    customer: str | None = None

    port: str | None = None

    vessel: str | None = None

    date: str | None = None

    priority: str | None = None

    document_type: str | None = None

    def to_dict(self):

        return asdict(self)

    def is_empty(self) -> bool:

        return not any(

            [

                self.shipment,

                self.email_id,

                self.customer,

                self.port,

                self.vessel,

                self.date,

                self.priority,

                self.document_type,

            ]

        )