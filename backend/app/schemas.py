from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    role: str
    display_name: str


class Place(BaseModel):
    id: str
    name: str
    category: str
    city: str
    description: str
    timings: str
    entry_fee: float
    price_band: str
    rating: float
    latitude: float
    longitude: float
    safety_score: int


class TripCreateRequest(BaseModel):
    user_name: str = Field(..., min_length=2)
    city: str
    start_date: str
    end_date: str
    travelers: int = Field(default=1, ge=1, le=10)
    interests: list[str] = Field(default_factory=list)


class TripResponse(BaseModel):
    id: str
    user_name: str
    city: str
    start_date: str
    end_date: str
    travelers: int
    interests: list[str]
    status: str
    created_at: str


class LocationUpdateRequest(BaseModel):
    traveler_name: str
    city: str
    latitude: float
    longitude: float
    panic_mode: bool = False


class SafetyScoreResponse(BaseModel):
    score: int
    level: str
    reasons: list[str]
    nearby_zone: str | None = None
    advice: str | None = None


class RouteRequest(BaseModel):
    origin_lat: float
    origin_lng: float
    destination_lat: float
    destination_lng: float
    mode: str = "driving"


class RouteResponse(BaseModel):
    route_id: str
    safety_score: int
    duration_minutes: int
    warnings: list[str]
    recommended_action: str


class SosRequest(BaseModel):
    traveler_name: str
    city: str
    latitude: float
    longitude: float
    message: str = Field(default="Need urgent assistance")
    trigger_method: str = Field(default="button")


class SosResponse(BaseModel):
    id: str
    status: str
    traveler_name: str
    city: str
    latitude: float
    longitude: float
    message: str
    trigger_method: str
    created_at: str


class IncidentRequest(BaseModel):
    traveler_name: str
    category: str
    city: str
    description: str
    latitude: float
    longitude: float
    severity: int = Field(default=3, ge=1, le=5)


class IncidentResponse(BaseModel):
    id: str
    traveler_name: str
    category: str
    city: str
    description: str
    latitude: float
    longitude: float
    severity: int
    status: str
    created_at: str


class NotificationItem(BaseModel):
    id: str
    type: str
    title: str
    message: str
    audience: str
    created_at: str


class EmergencyService(BaseModel):
    id: str
    name: str
    service_type: str
    city: str
    phone: str
    address: str
    latitude: float
    longitude: float
    is_verified: bool


class UnsafeZone(BaseModel):
    id: str
    title: str
    city: str
    zone_type: str
    severity: int
    latitude: float
    longitude: float
    radius_km: float
    advice: str
    active_from: str
    active_until: str


class UnsafeZoneCreateRequest(BaseModel):
    title: str
    city: str
    zone_type: str
    severity: int = Field(ge=1, le=5)
    latitude: float
    longitude: float
    radius_km: float = Field(default=1.0, gt=0)
    advice: str
    active_from: str
    active_until: str


class AdminDashboardSummary(BaseModel):
    active_trips: int
    open_incidents: int
    active_sos: int
    unsafe_zone_count: int
    verified_services: int
