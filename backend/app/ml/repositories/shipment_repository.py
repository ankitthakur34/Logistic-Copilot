from sqlalchemy import func
from datetime import date

from app.database.db import db
from app.models.shipment import Shipment
from app.models.container import Container
from app.models.port import Port
from app.models.task import Task
from app.models.vessel import Vessel




class ShipmentRepository:

    @staticmethod
    def get_prediction_features(shipment_no: str):

        shipment = (
            db.session.query(Shipment)
            .filter(Shipment.shipment_no == shipment_no)
            .first()
        )

        if shipment is None:
            return None

        vessel = (
            db.session.query(Vessel)
            .filter(Vessel.id == shipment.vessel_id)
            .first()
        )

        origin_port = (
            db.session.query(Port)
            .filter(Port.id == shipment.origin_port_id)
            .first()
        )

        destination_port = (
            db.session.query(Port)
            .filter(Port.id == shipment.destination_port_id)
            .first()
        )

        containers = (
            db.session.query(Container)
            .filter(Container.shipment_id == shipment.id)
            .all()
        )

        tasks = (
            db.session.query(Task)
            .filter(Task.shipment_id == shipment.id)
            .all()
        )

        # --------------------------
        # Containers
        # --------------------------

        container_count = len(containers)

        if container_count > 0:
            container_type = containers[0].type
        else:
            container_type = "Dry"

        # --------------------------
        # Tasks
        # --------------------------

        pending_tasks = sum(
            1 for task in tasks
            if task.status.lower() == "pending"
        )

        completed_tasks = sum(
            1 for task in tasks
            if task.status.lower() == "completed"
        )

        high_priority_tasks = sum(
    1 for task in tasks
    if task.priority.value == "HIGH"
)

        # --------------------------
        # ETA Remaining
        # --------------------------

        eta_remaining_days = max(
    (shipment.eta - date.today()).days,
    0,
)

        return {

            "shipment_no": shipment.shipment_no,

            "customer": shipment.customer,

            "shipment_status": shipment.status,

            "origin_port": origin_port.name,

            "destination_port": destination_port.name,

            "origin_country": origin_port.country,

            "destination_country": destination_port.country,

            "vessel_status": vessel.status,

            "container_count": container_count,

            "container_type": container_type,

            "pending_tasks": pending_tasks,

            "completed_tasks": completed_tasks,

            "high_priority_tasks": high_priority_tasks,

            "eta_remaining_days": max(
                eta_remaining_days,
                0,
            ),

            "maintenance_vessel": int(
                vessel.status == "Maintenance"
            ),

            "reefer_container": int(
                container_type == "Reefer"
            ),

            "has_many_pending_tasks": int(
                pending_tasks >= 4
            ),
        }