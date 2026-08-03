from app.ml.repositories.shipment_repository import ShipmentRepository
from app.ml.services.ml_service import MLPredictionService


class MLPredictionFacade:

    @staticmethod
    def predict(shipment_no: str):

        features = ShipmentRepository.get_prediction_features(
            shipment_no
        )

        if features is None:

            return {
                "success": False,
                "message": "Shipment not found."
            }

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

        return {

            "success": True,

            "shipment_no": shipment_no,

            "prediction": prediction["prediction"],

            "confidence": prediction["confidence"],

            "delay_probability":
                prediction["delay_probability"],

            "on_time_probability":
                prediction["on_time_probability"],

            "risk_factors": risk_factors
        }