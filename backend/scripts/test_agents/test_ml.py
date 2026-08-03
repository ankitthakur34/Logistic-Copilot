from app import create_app
from app.ml.repositories.shipment_repository import ShipmentRepository
from app.ml.services.ml_service import MLPredictionService




def main():

    app = create_app()

    with app.app_context():

        shipment_no = "SHP0005"

        print("=" * 60)
        print("Shipment")
        print("=" * 60)

        print(shipment_no)

        print()

        # -----------------------------------
        # Repository
        # -----------------------------------

        features = ShipmentRepository.get_prediction_features(
            shipment_no
        )

        if features is None:

            print("Shipment not found.")

            return

        print("=" * 60)
        print("Features")
        print("=" * 60)

        for key, value in features.items():
            print(f"{key:<25}: {value}")

        print()

        # -----------------------------------
        # ML Prediction
        # -----------------------------------

        prediction = MLPredictionService.predict_delay(
            features
        )

        print("=" * 60)
        print("Prediction")
        print("=" * 60)

        print(f"Prediction           : {prediction['prediction']}")
        print(f"Confidence           : {prediction['confidence']:.2%}")
        print(f"Delay Probability    : {prediction['delay_probability']:.2%}")
        print(f"On-Time Probability  : {prediction['on_time_probability']:.2%}")

        print("=" * 60)


if __name__ == "__main__":
    main()