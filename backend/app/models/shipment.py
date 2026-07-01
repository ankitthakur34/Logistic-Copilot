from app.database.db import db
from datetime import datetime

class Shipment(db.Model):

    __tablename__ = "shipments"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    shipment_no = db.Column(
        db.String(50),
        unique=True,
        nullable=False,
        index=True
    )

    customer = db.Column(
        db.String(100),
        nullable=False
    )

    status = db.Column(
        db.String(50),
        nullable=False
    )

    eta = db.Column(
        db.Date,
        nullable=False
    )

    vessel_id = db.Column(
        db.Integer,
        db.ForeignKey("vessels.id"),
        nullable=False
    )

    origin_port_id = db.Column(
        db.Integer,
        db.ForeignKey("ports.id"),
        nullable=False
    )

    destination_port_id = db.Column(
        db.Integer,
        db.ForeignKey("ports.id"),
        nullable=False
    )

    vessel = db.relationship(
        "Vessel",
        back_populates="shipments"
    )

    origin_port = db.relationship(
        "Port",
        foreign_keys=[origin_port_id],
        back_populates="origin_shipments"
    )

    destination_port = db.relationship(
        "Port",
        foreign_keys=[destination_port_id],
        back_populates="destination_shipments"
    )

    containers = db.relationship(
        "Container",
        back_populates="shipment",
        cascade="all, delete-orphan"
    )

    tasks = db.relationship(
        "Task",
        back_populates="shipment",
        cascade="all, delete-orphan"
    )
    created_at = db.Column(
    db.DateTime,
    default=datetime.utcnow
)

    updated_at = db.Column(
    db.DateTime,
    default=datetime.utcnow,
    onupdate=datetime.utcnow
)

    def __repr__(self):
        return f"<Shipment {self.shipment_no}>"