from app.database.db import db
from datetime import datetime

class Vessel(db.Model):

    __tablename__ = "vessels"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    imo = db.Column(
        db.String(20),
        unique=True,
        nullable=False,
        index=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    status = db.Column(
        db.String(50),
        nullable=False
    )

    shipments = db.relationship(
        "Shipment",
        back_populates="vessel",
        lazy=True
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
        return f"<Vessel {self.name}>"