from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True,
)

Base = declarative_base()


class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    probability_default = Column(Float, nullable=False)
    predicted_class = Column(Integer, nullable=False)
    threshold = Column(Float, nullable=False)
    risk_level = Column(String(32), nullable=False)
    payload_json = Column(Text, nullable=False)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)