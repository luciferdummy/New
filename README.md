# SMART TOURIST SAFETY AND TRAVEL ASSISTANT SYSTEM

A runnable hackathon MVP that now includes:

- a **FastAPI backend** for trips, alerts, safety scores, incidents, SOS, and admin operations
- a **tourist web frontend** for travel planning, safety checks, and emergency workflows
- an **admin web dashboard** for live monitoring, unsafe-zone publishing, and operations overview
- supporting architecture, API, schema, demo, and limitations documentation

## Working Product Surfaces

### Tourist Web App
- Demo tourist login
- Curated places feed
- Live alerts panel
- Emergency services panel
- Trip creation form
- Safety score / location check
- SOS trigger workflow
- Incident reporting form

### Admin Web Dashboard
- Demo admin login
- Operations summary KPIs
- Unsafe zone list
- SOS queue
- Incident queue
- Unsafe-zone creation form

### Backend API
Key endpoints:
- `GET /health`
- `POST /auth/login`
- `GET /places`
- `GET /support-services`
- `POST /trips`
- `GET /trips`
- `POST /location/update`
- `GET /safety/score`
- `POST /navigation/safe-route`
- `GET /alerts/feed`
- `POST /sos/trigger`
- `GET /sos`
- `POST /incidents`
- `GET /incidents`
- `GET /admin/dashboard/summary`
- `GET /admin/unsafe-zones`
- `POST /admin/unsafe-zones`
- `GET /admin/incidents`
- `GET /admin/sos`

## Demo Credentials

- Tourist: `tourist@demo.com` / `demo123`
- Admin: `admin@demo.com` / `admin123`

## Quick Start

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open:
- Tourist app: `http://127.0.0.1:8000/`
- Admin dashboard: `http://127.0.0.1:8000/admin`
- API docs: `http://127.0.0.1:8000/docs`

## Repository Structure

```text
android-app/           legacy Android anti-scam prototype from the original repo
backend/               live Smart Tourist Safety MVP backend + web frontend assets
docs/                  architecture, schema, API, demo, and limitations docs
```

## Product Scope

The system is designed to help tourists with:
- travel planning
- safe route and area awareness
- emergency response and SOS escalation
- verified help-center discovery
- admin-side monitoring and unsafe-zone control

## Documentation Map

- `docs/architecture.md`
- `docs/database-schema.md`
- `docs/api-spec.md`
- `docs/demo-walkthrough.md`
- `docs/limitations.md`
