from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import uuid4

UTC = timezone.utc


def now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


@dataclass
class TouristSafetyStore:
    places: list[dict[str, Any]] = field(default_factory=list)
    emergency_services: list[dict[str, Any]] = field(default_factory=list)
    unsafe_zones: list[dict[str, Any]] = field(default_factory=list)
    trips: list[dict[str, Any]] = field(default_factory=list)
    location_logs: list[dict[str, Any]] = field(default_factory=list)
    incidents: list[dict[str, Any]] = field(default_factory=list)
    sos_alerts: list[dict[str, Any]] = field(default_factory=list)
    notifications: list[dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.places:
            return

        self.places = [
            {
                "id": "place-hawa-mahal",
                "name": "Hawa Mahal",
                "category": "attraction",
                "city": "Jaipur",
                "description": "Historic palace with panoramic city views and strong tourist footfall.",
                "timings": "9:00 AM - 5:00 PM",
                "entry_fee": 50,
                "price_band": "budget",
                "rating": 4.7,
                "latitude": 26.9239,
                "longitude": 75.8267,
                "safety_score": 82,
            },
            {
                "id": "place-city-palace",
                "name": "City Palace",
                "category": "attraction",
                "city": "Jaipur",
                "description": "Royal heritage complex with curated guided-tour information.",
                "timings": "9:30 AM - 6:00 PM",
                "entry_fee": 200,
                "price_band": "mid",
                "rating": 4.8,
                "latitude": 26.9258,
                "longitude": 75.8237,
                "safety_score": 80,
            },
            {
                "id": "place-spice-court",
                "name": "Spice Court",
                "category": "restaurant",
                "city": "Jaipur",
                "description": "Popular restaurant with vegetarian and local Rajasthani menu guidance.",
                "timings": "12:00 PM - 11:00 PM",
                "entry_fee": 0,
                "price_band": "mid",
                "rating": 4.4,
                "latitude": 26.9107,
                "longitude": 75.8042,
                "safety_score": 76,
            },
            {
                "id": "place-amber-road-hotel",
                "name": "Amber Road Stay",
                "category": "hotel",
                "city": "Jaipur",
                "description": "Budget-friendly stay with 24/7 desk and tourist support.",
                "timings": "Open 24 hours",
                "entry_fee": 0,
                "price_band": "budget",
                "rating": 4.2,
                "latitude": 26.9312,
                "longitude": 75.8291,
                "safety_score": 79,
            },
        ]

        self.emergency_services = [
            {
                "id": "svc-police-1",
                "name": "Jaipur Tourist Police Help Desk",
                "service_type": "police",
                "city": "Jaipur",
                "phone": "+91-100",
                "address": "MI Road, Jaipur",
                "latitude": 26.9124,
                "longitude": 75.7873,
                "is_verified": True,
            },
            {
                "id": "svc-hospital-1",
                "name": "Sawai Man Singh Hospital",
                "service_type": "hospital",
                "city": "Jaipur",
                "phone": "+91-141-2518384",
                "address": "JLN Marg, Jaipur",
                "latitude": 26.8902,
                "longitude": 75.8155,
                "is_verified": True,
            },
            {
                "id": "svc-embassy-1",
                "name": "Foreign Tourist Help Center",
                "service_type": "help_center",
                "city": "Jaipur",
                "phone": "+91-141-2222222",
                "address": "Tourism Office, Jaipur",
                "latitude": 26.9050,
                "longitude": 75.8010,
                "is_verified": True,
            },
        ]

        self.unsafe_zones = [
            {
                "id": "zone-bapu-market",
                "title": "Bapu Market Evening Theft Risk",
                "city": "Jaipur",
                "zone_type": "theft",
                "severity": 4,
                "latitude": 26.9162,
                "longitude": 75.8208,
                "radius_km": 1.2,
                "advice": "Avoid isolated lanes after 8 PM and keep valuables hidden.",
                "active_from": now_iso(),
                "active_until": (datetime.now(UTC) + timedelta(days=1)).replace(microsecond=0).isoformat(),
            },
            {
                "id": "zone-protest-mi-road",
                "title": "Traffic Protest Diversion",
                "city": "Jaipur",
                "zone_type": "protest",
                "severity": 3,
                "latitude": 26.9128,
                "longitude": 75.8035,
                "radius_km": 0.8,
                "advice": "Expect congestion and use alternate route for tourist buses.",
                "active_from": now_iso(),
                "active_until": (datetime.now(UTC) + timedelta(hours=8)).replace(microsecond=0).isoformat(),
            },
        ]

        self.notifications = [
            {
                "id": "note-1",
                "type": "warning",
                "title": "High theft advisory",
                "message": "Crowded market areas are under active watch tonight. Prefer main roads.",
                "audience": "tourists",
                "created_at": now_iso(),
            },
            {
                "id": "note-2",
                "type": "info",
                "title": "Festival traffic update",
                "message": "City Palace approach roads may be slow from 6 PM to 9 PM.",
                "audience": "tourists",
                "created_at": now_iso(),
            },
        ]

    def _create_id(self, prefix: str) -> str:
        return f"{prefix}-{uuid4().hex[:8]}"

    def create_trip(self, payload: dict[str, Any]) -> dict[str, Any]:
        trip = {
            "id": self._create_id("trip"),
            "status": "planned",
            "created_at": now_iso(),
            **payload,
        }
        self.trips.append(trip)
        return trip

    def log_location(self, payload: dict[str, Any]) -> dict[str, Any]:
        event = {"id": self._create_id("loc"), "recorded_at": now_iso(), **payload}
        self.location_logs.append(event)
        return event

    def create_incident(self, payload: dict[str, Any]) -> dict[str, Any]:
        incident = {
            "id": self._create_id("incident"),
            "status": "open",
            "created_at": now_iso(),
            **payload,
        }
        self.incidents.append(incident)
        return incident

    def create_sos(self, payload: dict[str, Any]) -> dict[str, Any]:
        alert = {
            "id": self._create_id("sos"),
            "status": "active",
            "created_at": now_iso(),
            **payload,
        }
        self.sos_alerts.append(alert)
        return alert

    def add_notification(self, payload: dict[str, Any]) -> dict[str, Any]:
        item = {"id": self._create_id("note"), "created_at": now_iso(), **payload}
        self.notifications.insert(0, item)
        return item

    def add_unsafe_zone(self, payload: dict[str, Any]) -> dict[str, Any]:
        zone = {"id": self._create_id("zone"), **payload}
        self.unsafe_zones.insert(0, zone)
        return zone

    def dashboard_summary(self) -> dict[str, Any]:
        active_trips = sum(1 for trip in self.trips if trip.get("status") == "active")
        open_incidents = sum(1 for incident in self.incidents if incident.get("status") != "resolved")
        active_sos = sum(1 for alert in self.sos_alerts if alert.get("status") == "active")
        return {
            "active_trips": active_trips,
            "open_incidents": open_incidents,
            "active_sos": active_sos,
            "unsafe_zone_count": len(self.unsafe_zones),
            "verified_services": sum(1 for service in self.emergency_services if service.get("is_verified")),
        }


DB = TouristSafetyStore()
