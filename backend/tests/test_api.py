from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analyze_transaction_high_risk() -> None:
    response = client.post(
        "/analyze_transaction",
        json={
            "amount": 15000,
            "receiver": "Unknown Merchant",
            "upi_id": "fraudster@upi",
            "source": "SIMULATION",
            "message": "Urgent refund collect request. Click bit.ly/pay",
            "has_otp_context": True,
            "is_collect_request": True,
            "hour_of_day": 1,
            "average_amount": 1000,
            "recent_transaction_count": 6,
            "known_contacts": ["mom@upi"],
            "blacklisted_upi_ids": ["fraudster@upi"],
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["risk_level"] == "HIGH"
    assert body["risk_score"] >= 75


def test_analyze_message_extracts_metadata() -> None:
    response = client.post(
        "/analyze_message",
        json={"message": "URGENT refund pending. Share OTP 445566 and pay Rs 1200 via fraudster@upi"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["category"] in {"OTP", "SCAM"}
    assert body["contains_link"] is False
