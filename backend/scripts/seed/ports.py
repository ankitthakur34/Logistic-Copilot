from app.models.port import Port
from app.database.db import db


def seed_ports():

    if Port.query.count() > 0:
        print("port already seeded.")
        return

    ports = [

        Port(
            name="Nhava Sheva",
            country="India",
            code="INNSA"
        ),

        Port(
            name="Singapore",
            country="Singapore",
            code="SGSIN"
        ),

        Port(
            name="Rotterdam",
            country="Netherlands",
            code="NLRTM"
        ),

        Port(
            name="Shanghai",
            country="China",
            code="CNSHA"
        ),

        Port(
            name="Dubai",
            country="UAE",
            code="AEDXB"
        ),

        Port(
            name="Hamburg",
            country="Germany",
            code="DEHAM"
        )

    ]

    db.session.add_all(ports)
    db.session.commit()

    print("Ports Seeded")