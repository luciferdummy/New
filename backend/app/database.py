from dataclasses import dataclass, field
from typing import Any


@dataclass
class DemoDatabase:
    transaction_history: list[dict[str, Any]] = field(default_factory=list)
    known_contacts: list[str] = field(default_factory=lambda: ["mom@upi", "rentowner@oksbi", "friend@okaxis"])
    blacklisted_upi_ids: list[str] = field(default_factory=lambda: ["fraudster@upi", "scam.collect@oksbi"])
    scam_keywords: list[str] = field(default_factory=lambda: ["refund", "urgent", "verify", "reward", "collect"])
    risk_logs: list[dict[str, Any]] = field(default_factory=list)

    def log_transaction(self, payload: dict[str, Any]) -> None:
        self.transaction_history.append(payload)

    def log_risk(self, payload: dict[str, Any]) -> None:
        self.risk_logs.append(payload)


DB = DemoDatabase()
