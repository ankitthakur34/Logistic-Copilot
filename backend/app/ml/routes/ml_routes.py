from flask import Blueprint
from flask import jsonify
from flask import request

from app.ml.repositories.shipment_repository import ShipmentRepository
from app.ml.schemas.ml_schema import (
    ShipmentPredictionRequest,
    ShipmentPredictionResponse,
)
from app.ml.services.ml_service import MLPredictionService

ml_bp = Blueprint(
    "ml",
    __name__,
    url_prefix="/api/ml",
)
@ml_bp.route(
    "/predict-delay",
    methods=["POST"],
)
def predict_delay():

    body = ShipmentPredictionRequest(
        **request.get_json()
    )

    features = ShipmentRepository.get_prediction_features(
        body.shipment_no
    )

    if features is None:

        return jsonify({

            "message": "Shipment not found."

        }), 404

    prediction = MLPredictionService.predict_delay(
        features
    )

    risk_factors = []

    if features["maintenance_vessel"]:
        risk_factors.append(
            "Maintenance Vessel"
        )

    if features["reefer_container"]:
        risk_factors.append(
            "Reefer Container"
        )

    if features["has_many_pending_tasks"]:
        risk_factors.append(
            "Many Pending Tasks"
        )

    if features["eta_remaining_days"] <= 1:
        risk_factors.append(
            "Shipment Near ETA"
        )

    if features["high_priority_tasks"] >= 2:
        risk_factors.append(
            "Multiple High Priority Tasks"
        )

    response = ShipmentPredictionResponse.build(
        shipment_no=body.shipment_no,
        prediction=prediction,
        risk_factors=risk_factors,
    )

    return jsonify(response)