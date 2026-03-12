import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

MODELS_DIR = BASE_DIR / "models"

MODEL_PATH = Path(
    os.getenv("MODEL_PATH", str(MODELS_DIR / "catboost_credit_scoring.cbm"))
)
ARTIFACTS_PATH = Path(
    os.getenv("ARTIFACTS_PATH", str(MODELS_DIR / "catboost_artifacts.json"))
)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://credit_user:credit_pass@localhost:5432/credit_scoring",
)

APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "8000"))