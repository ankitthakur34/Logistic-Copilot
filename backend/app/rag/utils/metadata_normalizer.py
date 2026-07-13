from datetime import date, datetime


FIELD_ALIASES = {

    # shipment
    "shipment": "shipment_id",
    "shipment_id": "shipment_id",
    "shipmentnumber": "shipment_id",
    "shipment_number": "shipment_id",

    # order
    "order": "order_id",
    "order_id": "order_id",

    # customer
    "customer_name": "customer",
    "client": "customer",
    "customer": "customer",

    # eta
    "eta": "eta",
    "vessel_eta": "eta",
    "vessel.eta": "eta",

    # vessel
    "vessel_name": "vessel",
    "vessel.name": "vessel",
}


def normalize_metadata(metadata: dict):

    normalized = {}

    for key, value in metadata.items():

        if value is None:
            continue

        key = str(key).lower().strip()

        key = FIELD_ALIASES.get(
            key,
            key,
        )

        if isinstance(
            value,
            (date, datetime),
        ):
            value = value.isoformat()

        normalized[key] = value

    return normalized