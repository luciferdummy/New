from __future__ import annotations

from dataclasses import dataclass
import re

SCAM_KEYWORDS = ["refund", "urgent", "verify", "suspended", "collect", "reward", "kyc"]
SHORT_LINK_PATTERN = re.compile(r"bit\.ly|tinyurl|goo\.gl|https?://\S+", re.IGNORECASE)
UPI_PATTERN = re.compile(r"[a-zA-Z0-9._-]+@[a-zA-Z]+")
AMOUNT_PATTERN = re.compile(r"(?:₹|rs\.?|inr)\s?([0-9,]+(?:\.[0-9]{1,2})?)", re.IGNORECASE)


@dataclass
class RiskResult:
    risk_score: int
    risk_level: str
    reason: list[str]


class FraudEngine:
    def __init__(self) -> None:
        self.default_blacklist = {
            "fraudster@upi": "Known social engineering mule account",
            "scam.collect@oksbi": "Reported collect-request abuse",
        }

    def analyze_transaction(self, payload) -> RiskResult:
        score = 0
        reasons: list[str] = []
        amount = payload.amount or 0.0
        upi_id = (payload.upi_id or "").lower()
        message = payload.message or ""
        known_contacts = {contact.lower() for contact in payload.known_contacts}
        blacklist = {item.lower() for item in payload.blacklisted_upi_ids} | set(self.default_blacklist)

        if amount and amount > payload.average_amount * 3:
            score += 25
            reasons.append("Unusual amount")
        if upi_id and upi_id not in known_contacts:
            score += 20
            reasons.append("Unknown receiver")
        if any(keyword in message.lower() for keyword in SCAM_KEYWORDS):
            score += 15
            reasons.append("Scam keyword detected")
        if SHORT_LINK_PATTERN.search(message):
            score += 20
            reasons.append("Suspicious link detected")
        if payload.hour_of_day < 6 or payload.hour_of_day > 23:
            score += 10
            reasons.append("Late night transaction")
        if payload.recent_transaction_count >= 5:
            score += 10
            reasons.append("Too many transactions in a short time")
        if upi_id and upi_id in blacklist:
            score += 35
            reasons.append("Blacklisted UPI ID")
        if payload.has_otp_context:
            score += 15
            reasons.append("OTP received before payment")
        if payload.is_collect_request:
            score += 20
            reasons.append("Payment collect request detected")
        if payload.is_autopay:
            score += 10
            reasons.append("Autopay approval flow detected")

        return self._finalize(score, reasons)

    def analyze_message(self, message: str) -> RiskResult:
        lower = message.lower()
        score = 0
        reasons: list[str] = []
        if "otp" in lower or "one time password" in lower:
            score += 20
            reasons.append("OTP message detected")
        if any(keyword in lower for keyword in SCAM_KEYWORDS):
            score += 25
            reasons.append("Scam keyword detected")
        if SHORT_LINK_PATTERN.search(message):
            score += 20
            reasons.append("Suspicious link detected")
        if "debited" in lower or "credited" in lower:
            score += 10
            reasons.append("Banking or payment alert detected")
        return self._finalize(score, reasons)

    def blacklist_check(self, upi_id: str) -> dict:
        normalized = upi_id.lower()
        return {
            "upi_id": upi_id,
            "blacklisted": normalized in self.default_blacklist,
            "reason": self.default_blacklist.get(normalized),
        }

    def message_metadata(self, message: str) -> dict:
        lower = message.lower()
        category = "UNKNOWN"
        if "otp" in lower or "one time password" in lower:
            category = "OTP"
        elif "debited" in lower or "paid" in lower or "sent rs" in lower:
            category = "DEBIT"
        elif "credited" in lower or "received rs" in lower:
            category = "CREDIT"
        elif any(keyword in lower for keyword in SCAM_KEYWORDS):
            category = "SCAM"
        elif any(word in lower for word in ["offer", "sale", "discount", "cashback"]):
            category = "PROMOTION"

        amount_match = AMOUNT_PATTERN.search(message)
        amount = float(amount_match.group(1).replace(",", "")) if amount_match else None
        return {
            "category": category,
            "amount": amount,
            "keywords": [keyword for keyword in SCAM_KEYWORDS if keyword in lower],
            "contains_link": bool(SHORT_LINK_PATTERN.search(message)),
            "upi_ids": UPI_PATTERN.findall(message),
        }

    @staticmethod
    def _finalize(score: int, reasons: list[str]) -> RiskResult:
        score = max(0, min(score, 100))
        if score <= 30:
            level = "SAFE"
        elif score <= 60:
            level = "SUSPICIOUS"
        else:
            level = "HIGH"
        return RiskResult(risk_score=score, risk_level=level, reason=list(dict.fromkeys(reasons)) or ["No major fraud indicators detected"])
