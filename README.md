# SMART TOURIST SAFETY AND TRAVEL ASSISTANT SYSTEM

A runnable hackathon MVP that currently ships as a **full-stack web app**, including:

- a **FastAPI backend** for trips, alerts, safety scores, incidents, SOS, and admin operations
- a **tourist web app** for travel planning, safety checks, and emergency workflows
- an **admin web dashboard** for live monitoring, unsafe-zone publishing, and operations overview
- supporting architecture, API, schema, demo, and limitations documentation

## Preview Status

**Yes — this project is ready to preview as a local web MVP.**

Current preview surfaces:
- Tourist app: `http://127.0.0.1:8000/`
- Admin dashboard: `http://127.0.0.1:8000/admin`
- API docs: `http://127.0.0.1:8000/docs`

What “ready to preview” means here:
- the backend starts locally with FastAPI
- the tourist and admin pages are served from the same backend
- the demo flows for login, alerts, trips, SOS, incidents, and unsafe zones work with in-memory seeded data

What it does **not** mean:
- it is not production-ready
- it does not yet use a persistent database in the running app
- it does not yet include real police/maps/payment/telecom integrations

## What This Project Is

This implementation is currently a **web app + backend**, not a finished native Android or iOS tourist app.

- Tourist interface: browser-based web app served at `/`
- Admin interface: browser-based dashboard served at `/admin`
- Backend/API: FastAPI service
- Legacy Android code in `android-app/` is from the original repo and is not the active Smart Tourist Safety MVP

For a direct explanation, see `PROJECT-TYPE.md`.

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

## Why the "binary files not supported" message happened

That message appears when someone tries to review a generated `.zip` file directly in a code hosting UI.

A `.zip` file is a **binary artifact**, so many review tools cannot show a readable diff or preview for it. To avoid that problem, this repository now keeps the **zip out of git** and instead provides a script that generates it locally when you need it.

## How to get the zip

### Option 1: Download the whole repository as a zip
If your git hosting provider supports it, use the repository UI:
1. Open the repository page.
2. Click **Code**.
3. Click **Download ZIP**.

This gives you the full repository snapshot.

### Option 2: Generate the clean project zip locally
Run:

```bash
python scripts/create_download_bundle.py
```

This creates:
- `dist/smart-tourist-safety-web-mvp/`
- `dist/smart-tourist-safety-web-mvp.zip`

The generated zip includes only the active MVP deliverables:
- `README.md`
- `PROJECT-TYPE.md`
- `NEEDTOCHANGE.md`
- `backend/`
- `docs/`

## What to change manually

A dedicated manual-change guide is available in:

- `NEEDTOCHANGE.md`

Use that file as your checklist for moving this hackathon MVP toward a cleaner production-style implementation.

## Repository Structure

```text
android-app/           legacy Android anti-scam prototype from the original repo
backend/               live Smart Tourist Safety MVP backend + web frontend assets
docs/                  architecture, schema, API, demo, and limitations docs
scripts/               packaging helper to create the downloadable MVP zip
dist/                  generated output folder (ignored in git)
NEEDTOCHANGE.md        manual cleanup / replacement guide for the MVP
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
