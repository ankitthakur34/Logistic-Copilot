from pydantic import BaseModel


class ShipmentPredictionRequest(BaseModel):
    shipment_no: str

class ShipmentPredictionResponse:

    @staticmethod
    def build(
        shipment_no: str,
        prediction: dict,
        risk_factors: list[str],
    ):

        return {

            "shipment_no": shipment_no,

            "prediction": prediction["prediction"],

            "confidence": prediction["confidence"],

            "delay_probability": prediction["delay_probability"],

            "on_time_probability": prediction["on_time_probability"],

            "risk_factors": risk_factors,
        }