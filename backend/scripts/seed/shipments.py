import random
from datetime import date, timedelta

from app.database.db import db
from app.models.shipment import Shipment
from app.models.port import Port
from app.models.vessel import Vessel


def seed_shipments():

    if Shipment.query.count() > 0:
        print("Shipments already seeded.")
        return

    ports = Port.query.all()
    vessels = Vessel.query.all()

    customers = [
        "Samsung India",
        "Apple",
        "Tesla",
        "Reliance Retail",
        "Tata Steel",
        "IKEA",
        "Amazon",
        "Unilever",
        "Nestle",
        "Adidas"
    ]

    statuses = [
        "Booked",
        "At Origin Port",
        "In Transit",
        "Delayed",
        "Customs Clearance",
        "Delivered"
    ]

    shipments = []

    for i in range(1, 13):

        origin = random.choice(ports)

        destination = random.choice(ports)

        while origin.id == destination.id:
            destination = random.choice(ports)

        shipment = Shipment(

            shipment_no=f"SHP{i:04d}",

            customer=random.choice(customers),

            status=random.choice(statuses),

            eta=date.today() + timedelta(
                days=random.randint(2, 25)
            ),

            vessel_id=random.choice(vessels).id,

            origin_port_id=origin.id,

            destination_port_id=destination.id

        )

        shipments.append(shipment)

    db.session.add_all(shipments)

    db.session.commit()

    print("Shipments Seeded Successfully")