import random
from datetime import date, timedelta

from app.database.db import db

from app.models.task import Task
from app.models.user import User
from app.models.shipment import Shipment
from app.models.task import TaskPriority


def seed_tasks():

    if Task.query.count() > 0:
        print("Tasks already seeded.")
        return

    users = User.query.all()

    shipments = Shipment.query.all()

    titles = [

        "Verify Shipping Documents",

        "Customs Clearance",

        "Container Inspection",

        "Schedule Vessel Loading",

        "Update Customer",

        "Generate Invoice",

        "Check Dangerous Goods",

        "Confirm Delivery Appointment"

    ]

    statuses = [

        "Pending",

        "In Progress",

        "Completed"

    ]

    priorities = [

        TaskPriority.LOW,

        TaskPriority.MEDIUM,

        TaskPriority.HIGH

    ]

    tasks = []

    for shipment in shipments:

        total = random.randint(1, 3)

        for _ in range(total):

            task = Task(

                title=random.choice(titles),

                priority=random.choice(priorities),

                status=random.choice(statuses),

                due_date=date.today() + timedelta(
                    days=random.randint(1, 10)
                ),

                shipment_id=shipment.id,

                owner_id=random.choice(users).id

            )

            tasks.append(task)

    db.session.add_all(tasks)

    db.session.commit()

    print("Tasks Seeded Successfully")