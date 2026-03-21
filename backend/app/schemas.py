from pydantic import BaseModel, Field


class TransactionRequest(BaseModel):
    amount: float | None = None
    receiver: str | None = None
    upi_id: str | None = None
    source: str = Field(default="ACCESSIBILITY")
    message: str | None = None
    has_otp_context: bool = False
    is_collect_request: bool = False
    is_autopay: bool = False
    hour_of_day: int = 12
    average_amount: float = 1000.0
    recent_transaction_count: int = 0
    known_contacts: list[str] = Field(default_factory=list)
    blacklisted_upi_ids: list[str] = Field(default_factory=list)


class MessageRequest(BaseModel):
    message: str


class RiskResponse(BaseModel):
    risk_score: int
    risk_level: str
    reason: list[str]
