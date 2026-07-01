from app.database.db import db
from app.models.vessel import Vessel


def seed_vessels():

    if Vessel.query.count() > 0:
        print("Vessels already seeded.")
        return

    vessels = [

        Vessel(
            imo="9387421",
            name="MV Maersk Horizon",
            status="At Sea"
        ),

        Vessel(
            imo="9478210",
            name="MV Blue Ocean",
            status="Available"
        ),

        Vessel(
            imo="9654321",
            name="MV Pacific Carrier",
            status="Docked"
        ),

        Vessel(
            imo="9723489",
            name="MV Baltic Star",
            status="Maintenance"
        )

    ]

    db.session.add_all(vessels)

    db.session.commit()

    print("Vessels Seeded Successfully")