from app.database.db import db
import datetime
import enum

class TaskPriority(enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class Task(db.Model):

    __tablename__ = "tasks"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    priority = db.Column(
    db.Enum(TaskPriority),
    nullable=False
)

    status = db.Column(
        db.String(30),
        nullable=False
    )

    due_date = db.Column(
        db.Date,
        nullable=False
    )

    shipment_id = db.Column(
        db.Integer,
        db.ForeignKey("shipments.id"),
        nullable=False
    )

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    shipment = db.relationship(
        "Shipment",
        back_populates="tasks"
    )

    owner = db.relationship(
        "User",
        back_populates="tasks"
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
        return f"<Task {self.title}>"