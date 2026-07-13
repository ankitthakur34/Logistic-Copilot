FIELD_ALIASES = {

    #
    # Shipment
    #
    "shipment": "shipment_id",
    "shipmentid": "shipment_id",
    "shipment_no": "shipment_id",
    "shipment_number": "shipment_id",
    "shipment_ref": "shipment_id",

    #
    # Customer
    #
    "customer_name": "customer",
    "client": "customer",
    "customerid": "customer",

    #
    # Order
    #
    "order": "order_id",
    "order_no": "order_id",
    "order_number": "order_id",

    #
    # ETA
    #
    "eta": "vessel.eta",
    "estimated_arrival": "vessel.eta",

    #
    # Vessel
    #
    "vessel_name": "vessel.name",
}


class MetadataNormalizer:

    @classmethod
    def normalize_key(
        cls,
        key: str,
    ):

        key = key.lower().strip()

        return FIELD_ALIASES.get(
            key,
            key,
        )

    @classmethod
    def normalize_metadata(
        cls,
        metadata: dict,
    ):

        normalized = {}

        for key, value in metadata.items():

            normalized_key = cls.normalize_key(
                key
            )

            normalized[
                normalized_key
            ] = value

        return normalized