import random

from app.database.db import db
from app.models.container import Container
from app.models.shipment import Shipment


def seed_containers():

    if Container.query.count() > 0:
        print("Containers already seeded.")
        return

    shipments = Shipment.query.all()

    sizes = [
        "20FT",
        "40FT"
    ]

    types = [
        "Dry",
        "Reefer",
        "Open Top",
        "Flat Rack"
    ]

    statuses = [
        "At Origin Port",
        "Loaded",
        "In Transit",
        "At Destination Port",
        "Delivered"
    ]

    containers = []

    container_number = 100001

    for shipment in shipments:

        # Every shipment has 2–4 containers
        total = random.randint(2, 4)

        for _ in range(total):

            container = Container(

                container_no=f"MSCU{container_number}",

                size=random.choice(sizes),

                type=random.choice(types),

                status=random.choice(statuses),

                shipment_id=shipment.id

            )

            containers.append(container)

            container_number += 1

    db.session.add_all(containers)

    db.session.commit()

    print("Containers Seeded Successfully")