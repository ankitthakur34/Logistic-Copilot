from app.database.db import db
from datetime import datetime

class Port(db.Model):

    __tablename__ = "ports"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    code = db.Column(
        db.String(20),
        unique=True,
        nullable=False,
        index=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    country = db.Column(
        db.String(100),
        nullable=False
    )

    origin_shipments = db.relationship(
        "Shipment",
        foreign_keys="Shipment.origin_port_id",
        back_populates="origin_port"
    )

    destination_shipments = db.relationship(
        "Shipment",
        foreign_keys="Shipment.destination_port_id",
        back_populates="destination_port"
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
        return f"<Port {self.code}>"