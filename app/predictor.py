import pandas as pd

from app.model_loader import get_model_and_artifacts
from app.schemas import CreditScoringRequest


def get_risk_level(probability_default: float) -> str:
    if probability_default >= 0.70:
        return "high"
    if probability_default >= 0.40:
        return "medium"
    return "low"


def build_feature_frame(
    payload: CreditScoringRequest,
    feature_names: list[str],
    categorical_features: list[str],
) -> pd.DataFrame:
    row = payload.model_dump()
    frame = pd.DataFrame([row])

    missing_columns = [column for column in feature_names if column not in frame.columns]
    if missing_columns:
        raise ValueError(f"Missing columns for inference: {missing_columns}")

    frame = frame[feature_names].copy()

    for column in categorical_features:
        if column in frame.columns:
            frame[column] = frame[column].astype(str)

    return frame


def make_prediction(payload: CreditScoringRequest) -> dict:
    model, artifacts = get_model_and_artifacts()

    feature_names = artifacts.get("feature_names", [])
    categorical_features = artifacts.get("categorical_features", [])
    threshold = float(artifacts.get("threshold", 0.5))

    if not feature_names:
        raise ValueError("Feature names are missing in catboost_artifacts.json")

    frame = build_feature_frame(payload, feature_names, categorical_features)

    probability_default = float(model.predict_proba(frame)[0][1])
    predicted_class = int(probability_default >= threshold)
    risk_level = get_risk_level(probability_default)

    return {
        "probability_default": probability_default,
        "predicted_class": predicted_class,
        "threshold": threshold,
        "risk_level": risk_level,
        "model_name": "catboost_credit_scoring",
    }