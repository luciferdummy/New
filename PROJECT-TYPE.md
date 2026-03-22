# Current Delivery Type

## What this project is right now

This repository currently delivers a **web-based full-stack MVP**, not a native mobile app.

### Included right now
- **Tourist web app** served from FastAPI at `/`
- **Admin web dashboard** served from FastAPI at `/admin`
- **Backend API** served from FastAPI for trips, alerts, safety scoring, SOS, incidents, and admin operations
- **Documentation bundle** in `docs/`

### Not included as part of the current runnable MVP
- A finished native Android tourist app
- A finished iOS app
- A production deployment setup
- Persistent database storage

## Why there is still an `android-app/` folder

The `android-app/` directory is a **legacy prototype from the original repository topic** and is **not the current Smart Tourist Safety MVP delivery target**.

If you want, this web MVP can be converted later into:
1. a React Native app,
2. a Flutter app, or
3. a PWA/mobile-first web app.

## Recommended way to describe this project

Use this wording:

> **Smart Tourist Safety and Travel Assistant is currently a full-stack web MVP with a tourist-facing web app, an admin dashboard, and a FastAPI backend.**

That is the most accurate description of what is implemented in this repository today.
