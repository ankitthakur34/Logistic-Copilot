from app.ml.model_loader import MLModelLoader

import pandas as pd


class MLPredictionService:

    @staticmethod
    def predict_delay(features):

        df = pd.DataFrame([features])

        for column, encoder in MLModelLoader.label_encoders.items():

            if column not in df.columns:
                continue

            value = str(df.at[0, column])

            if value not in encoder.classes_:
                value = encoder.classes_[0]

            df[column] = encoder.transform([value])

        df = df[
            MLModelLoader.feature_columns
        ]

        prediction = MLModelLoader.model.predict(df)[0]

        probability = MLModelLoader.model.predict_proba(df)[0]

        confidence = float(max(probability))

        return {

            "prediction":
                "Delayed"
                if prediction
                else "On Time",

            "prediction_code":
                int(prediction),

            "confidence":
                round(confidence,4),

            "delay_probability":
                round(float(probability[1]),4),

            "on_time_probability":
                round(float(probability[0]),4)

        }