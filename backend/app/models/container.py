from app.database.db import db
from datetime import datetime
class Container(db.Model):

    __tablename__ = "containers"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    container_no = db.Column(
        db.String(20),
        unique=True,
        nullable=False,
        index=True
    )

    size = db.Column(
        db.String(10),
        nullable=False
    )

    type = db.Column(
        db.String(30),
        nullable=False
    )

    status = db.Column(
        db.String(30),
        nullable=False
    )

    shipment_id = db.Column(
        db.Integer,
        db.ForeignKey("shipments.id"),
        nullable=False
    )

    shipment = db.relationship(
        "Shipment",
        back_populates="containers"
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
        return f"<Container {self.container_no}>"