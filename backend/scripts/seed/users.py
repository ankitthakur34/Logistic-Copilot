from app.models.user import User
from app.database.db import db


def seed_users():

    if User.query.count() > 0:
        print("user already seeded.")
        return

    users = [

        User(
            name="Ankit",
            email="ankit@maersk.com",
            role="Operations Manager"
        ),

        User(
            name="Raj",
            email="raj@maersk.com",
            role="Customs Officer"
        ),

        User(
            name="Priya",
            email="priya@maersk.com",
            role="Logistics Coordinator"
        ),

        User(
            name="John",
            email="john@maersk.com",
            role="Port Manager"
        )

    ]

    db.session.add_all(users)
    db.session.commit()

    print("Users Seeded")