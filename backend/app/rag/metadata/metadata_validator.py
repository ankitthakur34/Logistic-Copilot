from app.rag.metadata.metadata_result import (
    MetadataResult,
)

from app.rag.metadata.metadata_schema import (
    MetadataSchema,
)

from app.rag.metadata.metadata_matcher import (
    MetadataMatcher,
)


class MetadataValidator:

    FIELD_ALIASES = {

        #
        # Shipment
        #
        "shipment": "shipment_id",
        "shipment_no": "shipment_id",
        "shipment_number": "shipment_id",

        #
        # Container
        #
        "container": "container_id",
        "container_no": "container_id",
        "container_number": "container_id",

        #
        # Invoice
        #
        "invoice": "invoice_id",
        "invoice_no": "invoice_id",

        #
        # Incident
        #
        "incident": "incident_id",
        "incident_no": "incident_id",

        #
        # Email
        #
        "email": "email_id",

        #
        # Booking
        #
        "booking": "booking_id",

        #
        # Tracking
        #
        "tracking": "tracking_id",

        #
        # Customer aliases
        #
        "client": "customer",
        "customer_name": "customer",

        #
        # ETA aliases
        #
        "eta": "vessel.eta",
    }

    NON_FUZZY_FIELDS = {

        "shipment_id",

        "incident_id",

        "container_id",

        "invoice_id",

        "booking_id",

        "tracking_id",

        "email_id",

        "date",
    }

    def __init__(
        self,
        schema: MetadataSchema,
    ):
        self.schema = schema

    def validate(
        self,
        metadata: MetadataResult,
    ) -> MetadataResult:

        validated = MetadataResult()

        print()
        print("=" * 80)
        print("RAW METADATA")
        print(metadata)
        print("=" * 80)

        for field_name, value in metadata.to_dict().items():

            ##################################################
            # EMPTY
            ##################################################

            if value is None:
                continue

            ##################################################
            # FIELD ALIAS
            ##################################################

            field_name = (
                self.FIELD_ALIASES.get(
                    field_name,
                    field_name,
                )
            )

            ##################################################
            # UNKNOWN FIELD
            ##################################################

            if not self.schema.has_field(
                field_name
            ):

                print(
                    f"[VALIDATOR] Unknown field : "
                    f"{field_name}"
                )

                continue

            allowed_values = (

                self.schema.allowed_values(
                    field_name
                )

            )

            print()
            print(
                f"{field_name} -> {value}"
            )
            print(
                "Allowed:",
                allowed_values,
            )

            ##################################################
            # NO VALUES
            ##################################################

            if not allowed_values:

                validated.set(
                    field_name,
                    value,
                )

                continue

            ##################################################
            # EXACT MATCH
            ##################################################

            if value in allowed_values:

                validated.set(
                    field_name,
                    value,
                )

                continue

            ##################################################
            # PRESERVE IDS
            ##################################################

            if (

                field_name
                in self.NON_FUZZY_FIELDS

            ):

                print(
                    f"[VALIDATOR] "
                    f"Preserving "
                    f"{field_name}={value}"
                )

                validated.set(
                    field_name,
                    value,
                )

                continue

            ##################################################
            # FUZZY MATCH
            ##################################################

            matched = MetadataMatcher.match(

                value=value,

                candidates=list(
                    allowed_values
                ),
            )

            if matched:

                validated.set(
                    field_name,
                    matched,
                )

        print()
        print("=" * 80)
        print("VALIDATED")
        print(validated)
        print("=" * 80)

        return validated