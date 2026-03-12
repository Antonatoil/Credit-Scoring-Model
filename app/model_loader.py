import json

from catboost import CatBoostClassifier

from app.config import ARTIFACTS_PATH, MODEL_PATH

_model = None
_artifacts = None


def get_model_and_artifacts():
    global _model
    global _artifacts

    if _model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Model file not found: {MODEL_PATH}. "
                "Run the training notebook first."
            )

        _model = CatBoostClassifier()
        _model.load_model(str(MODEL_PATH))

    if _artifacts is None:
        if not ARTIFACTS_PATH.exists():
            raise FileNotFoundError(
                f"Artifacts file not found: {ARTIFACTS_PATH}. "
                "Run the training notebook first."
            )

        with open(ARTIFACTS_PATH, "r", encoding="utf-8") as file:
            _artifacts = json.load(file)

    return _model, _artifacts