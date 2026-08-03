import os
import joblib


class MLModelLoader:

    model = None
    label_encoders = None
    feature_columns = None
    loaded = False

    @classmethod
    def load(cls, app):

        if cls.loaded:
            return

        model_dir = os.path.join(
            app.root_path,
            "ml",
            "models",
        )

        cls.model = joblib.load(
            os.path.join(
                model_dir,
                "shipment_delay_model.pkl",
            )
        )

        cls.label_encoders = joblib.load(
            os.path.join(
                model_dir,
                "label_encoders.pkl",
            )
        )

        cls.feature_columns = joblib.load(
            os.path.join(
                model_dir,
                "feature_columns.pkl",
            )
        )

        cls.loaded = True

        print(f"✅ ML Model Loaded from {model_dir}")