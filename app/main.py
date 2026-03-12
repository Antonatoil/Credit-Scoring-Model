import json

from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.database import PredictionLog, SessionLocal, init_db
from app.model_loader import get_model_and_artifacts
from app.predictor import make_prediction
from app.schemas import CreditScoringRequest, CreditScoringResponse

app = FastAPI(
    title="Credit Scoring Model API",
    description="API for credit default prediction using CatBoost",
    version="1.0.0",
)


@app.on_event("startup")
def startup_event() -> None:
    init_db()
    get_model_and_artifacts()


@app.get("/health")
def healthcheck() -> dict:
    model, artifacts = get_model_and_artifacts()
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "artifacts_loaded": artifacts is not None,
    }


@app.post("/predict", response_model=CreditScoringResponse)
def predict(payload: CreditScoringRequest) -> CreditScoringResponse:
    try:
        result = make_prediction(payload)

        db = SessionLocal()
        try:
            log = PredictionLog(
                probability_default=result["probability_default"],
                predicted_class=result["predicted_class"],
                threshold=result["threshold"],
                risk_level=result["risk_level"],
                payload_json=json.dumps(payload.model_dump(), ensure_ascii=False),
            )
            db.add(log)
            db.commit()
        except SQLAlchemyError as exc:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {exc}") from exc
        finally:
            db.close()

        return CreditScoringResponse(**result)

    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc