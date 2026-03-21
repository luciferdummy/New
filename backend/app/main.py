from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .database import DB
from .schemas import (
    AdminDashboardSummary,
    EmergencyService,
    IncidentRequest,
    IncidentResponse,
    LocationUpdateRequest,
    LoginRequest,
    LoginResponse,
    NotificationItem,
    Place,
    RouteRequest,
    RouteResponse,
    SafetyScoreResponse,
    SosRequest,
    SosResponse,
    TripCreateRequest,
    TripResponse,
    UnsafeZone,
    UnsafeZoneCreateRequest,
)

app = FastAPI(title="Smart Tourist Safety and Travel Assistant API", version="2.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


DEMO_USERS = {
    "tourist@demo.com": {"password": "demo123", "role": "tourist", "display_name": "Alex Tourist"},
    "admin@demo.com": {"password": "admin123", "role": "admin", "display_name": "City Operations Admin"},
}


def _distance_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    return ((lat1 - lat2) ** 2 + (lng1 - lng2) ** 2) ** 0.5 * 111


def compute_safety(lat: float, lng: float) -> dict[str, Any]:
    score = 88
    reasons = ["Route is being monitored against admin-defined unsafe zones."]
    nearby_zone: dict[str, Any] | None = None

    for zone in DB.unsafe_zones:
        distance = _distance_km(lat, lng, zone["latitude"], zone["longitude"])
        if distance <= zone["radius_km"]:
            zone_penalty = zone["severity"] * 12
            score -= zone_penalty
            nearby_zone = zone
            reasons.append(f"Inside or near unsafe zone: {zone['title']}.")
        elif distance <= zone["radius_km"] + 0.8:
            zone_penalty = zone["severity"] * 6
            score -= zone_penalty
            nearby_zone = nearby_zone or zone
            reasons.append(f"Approaching caution area: {zone['title']}.")

    if lat and lng and lat < 26.90:
        score -= 8
        reasons.append("Southern corridor currently has slower response coverage.")

    score = max(18, min(96, score))
    if score >= 75:
        level = "LOW"
    elif score >= 50:
        level = "MEDIUM"
    else:
        level = "HIGH"

    return {
        "score": score,
        "level": level,
        "reasons": reasons,
        "nearby_zone": nearby_zone["title"] if nearby_zone else None,
        "advice": nearby_zone["advice"] if nearby_zone else "Stay on primary roads and keep location sharing enabled.",
    }


@app.get("/", include_in_schema=False)
def tourist_ui() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/admin", include_in_schema=False)
def admin_ui() -> FileResponse:
    return FileResponse(STATIC_DIR / "admin.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "smart-tourist-safety-and-travel-assistant-api"}


@app.post("/auth/login", response_model=LoginResponse)
def login(payload: LoginRequest) -> dict[str, str]:
    user = DEMO_USERS.get(payload.email.lower())
    if not user or user["password"] != payload.password:
        raise HTTPException(status_code=401, detail="Invalid demo credentials")
    return {
        "access_token": f"demo-token-{user['role']}",
        "role": user["role"],
        "display_name": user["display_name"],
    }


@app.get("/places", response_model=list[Place])
def get_places(city: str | None = Query(default=None), category: str | None = Query(default=None)) -> list[dict[str, Any]]:
    places = DB.places
    if city:
        places = [place for place in places if place["city"].lower() == city.lower()]
    if category:
        places = [place for place in places if place["category"].lower() == category.lower()]
    return places


@app.get("/support-services", response_model=list[EmergencyService])
def get_support_services(city: str | None = Query(default=None), service_type: str | None = Query(default=None)) -> list[dict[str, Any]]:
    services = DB.emergency_services
    if city:
        services = [service for service in services if service["city"].lower() == city.lower()]
    if service_type:
        services = [service for service in services if service["service_type"].lower() == service_type.lower()]
    return services


@app.post("/trips", response_model=TripResponse)
def create_trip(payload: TripCreateRequest) -> dict[str, Any]:
    return DB.create_trip(payload.model_dump())


@app.get("/trips", response_model=list[TripResponse])
def list_trips() -> list[dict[str, Any]]:
    return DB.trips


@app.post("/location/update")
def location_update(payload: LocationUpdateRequest) -> dict[str, Any]:
    DB.log_location(payload.model_dump())
    safety = compute_safety(payload.latitude, payload.longitude)
    return {
        "message": "Location received",
        "panic_mode": payload.panic_mode,
        "traveler_name": payload.traveler_name,
        "safety": safety,
    }


@app.get("/safety/score", response_model=SafetyScoreResponse)
def safety_score(lat: float, lng: float) -> dict[str, Any]:
    return compute_safety(lat, lng)


@app.post("/navigation/safe-route", response_model=RouteResponse)
def navigation_safe_route(payload: RouteRequest) -> dict[str, Any]:
    route_safety = compute_safety(payload.destination_lat, payload.destination_lng)
    duration = int(_distance_km(payload.origin_lat, payload.origin_lng, payload.destination_lat, payload.destination_lng) * 5) + 10
    warnings = route_safety["reasons"][:]
    if route_safety["level"] != "LOW":
        warnings.append("Alternate route suggested to reduce exposure near flagged zones.")
        recommendation = "Use the safer highlighted route and avoid stopping in caution areas."
    else:
        recommendation = "Preferred route is acceptable; continue with periodic check-ins enabled."

    return {
        "route_id": f"route-{abs(hash((payload.origin_lat, payload.destination_lat, payload.mode))) % 10000}",
        "safety_score": route_safety["score"],
        "duration_minutes": duration,
        "warnings": warnings,
        "recommended_action": recommendation,
    }


@app.get("/alerts/feed", response_model=list[NotificationItem])
def alerts_feed() -> list[dict[str, Any]]:
    return DB.notifications


@app.post("/sos/trigger", response_model=SosResponse)
def trigger_sos(payload: SosRequest) -> dict[str, Any]:
    alert = DB.create_sos(payload.model_dump())
    DB.add_notification(
        {
            "type": "critical",
            "title": f"SOS triggered by {payload.traveler_name}",
            "message": payload.message,
            "audience": "admins",
        }
    )
    return alert


@app.get("/sos", response_model=list[SosResponse])
def list_sos() -> list[dict[str, Any]]:
    return DB.sos_alerts


@app.post("/incidents", response_model=IncidentResponse)
def create_incident(payload: IncidentRequest) -> dict[str, Any]:
    incident = DB.create_incident(payload.model_dump())
    DB.add_notification(
        {
            "type": "warning",
            "title": f"New {payload.category} incident",
            "message": payload.description,
            "audience": "admins",
        }
    )
    return incident


@app.get("/incidents", response_model=list[IncidentResponse])
def list_incidents() -> list[dict[str, Any]]:
    return DB.incidents


@app.get("/notifications", response_model=list[NotificationItem])
def list_notifications(audience: str | None = Query(default=None)) -> list[dict[str, Any]]:
    if not audience:
        return DB.notifications
    return [note for note in DB.notifications if note["audience"] in {audience, "tourists", "admins"}]


@app.get("/admin/dashboard/summary", response_model=AdminDashboardSummary)
def admin_dashboard_summary() -> dict[str, Any]:
    return DB.dashboard_summary()


@app.get("/admin/unsafe-zones", response_model=list[UnsafeZone])
def admin_unsafe_zones() -> list[dict[str, Any]]:
    return DB.unsafe_zones


@app.post("/admin/unsafe-zones", response_model=UnsafeZone)
def admin_create_unsafe_zone(payload: UnsafeZoneCreateRequest) -> dict[str, Any]:
    zone = DB.add_unsafe_zone(payload.model_dump())
    DB.add_notification(
        {
            "type": "warning",
            "title": f"Zone alert: {payload.title}",
            "message": payload.advice,
            "audience": "tourists",
        }
    )
    return zone


@app.get("/admin/incidents", response_model=list[IncidentResponse])
def admin_list_incidents() -> list[dict[str, Any]]:
    return DB.incidents


@app.get("/admin/sos", response_model=list[SosResponse])
def admin_list_sos() -> list[dict[str, Any]]:
    return DB.sos_alerts
