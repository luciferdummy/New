from fastapi import FastAPI

from .database import DB
from .fraud_engine import FraudEngine
from .schemas import MessageRequest, RiskResponse, TransactionRequest

app = FastAPI(title="Anti-Scam Payment Protection API", version="1.0.0")
engine = FraudEngine()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "anti-scam-payment-protection-api"}


@app.post("/analyze_transaction", response_model=RiskResponse)
def analyze_transaction(payload: TransactionRequest):
    result = engine.analyze_transaction(payload)
    DB.log_transaction(payload.model_dump())
    DB.log_risk(result.__dict__)
    return result.__dict__


@app.post("/analyze_message")
def analyze_message(payload: MessageRequest):
    result = engine.analyze_message(payload.message)
    metadata = engine.message_metadata(payload.message)
    DB.log_risk({"message": payload.message, **result.__dict__, **metadata})
    return {**result.__dict__, **metadata}


@app.post("/risk_score", response_model=RiskResponse)
def risk_score(payload: TransactionRequest):
    return engine.analyze_transaction(payload).__dict__


@app.get("/blacklist_check/{upi_id}")
def blacklist_check(upi_id: str):
    return engine.blacklist_check(upi_id)
