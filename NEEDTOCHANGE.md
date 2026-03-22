# NEED TO CHANGE / MANUAL IMPROVEMENT GUIDE

This file is the manual checklist for improving the current **Smart Tourist Safety and Travel Assistant** MVP.

## 1. Delivery type is web MVP, not native mobile
Right now the runnable product is:
- tourist web app
- admin web dashboard
- FastAPI backend

If you want a real mobile app later, you will need to rebuild the client in:
- Flutter, or
- React Native, or
- native Android/iOS

## 2. Replace demo authentication
Current state:
- credentials are hardcoded demo users in `backend/app/main.py`
- there is no real signup flow
- there is no JWT refresh, password reset, or session storage strategy

Manual changes needed:
- add user registration
- hash passwords
- move secrets to environment variables
- add role-based auth middleware
- add proper admin authorization checks

## 3. Replace in-memory storage with a real database
Current state:
- runtime data is stored in memory in `backend/app/database.py`
- data resets when the server restarts

Manual changes needed:
- connect FastAPI to PostgreSQL / MySQL / SQLite
- add ORM or SQL layer
- persist trips, incidents, SOS alerts, notifications, and unsafe zones
- add migrations

## 4. Replace mocked safety logic
Current state:
- safety score is based on simple local logic in `backend/app/main.py`
- unsafe zones are seeded manually

Manual changes needed:
- connect real map/routing services
- add geospatial queries
- use live zone/event data
- calculate routes from mapping APIs instead of demo logic

## 5. Replace seeded content
Current state:
- places, support services, notifications, and zones are seeded in code
- city data is demo-only

Manual changes needed:
- move places and services into the database
- connect admin CRUD to persistent storage
- load real city/tourism/emergency records

## 6. Improve frontend architecture
Current state:
- frontend uses static HTML + CSS + vanilla JavaScript
- suitable for demo, but limited for scaling

Manual changes needed:
- optionally move UI to React / Next.js / Vue
- add reusable components
- add client-side validation and better state management
- improve responsiveness and UX polish

## 7. Remove or archive legacy anti-scam parts
Current state:
- `android-app/` is from the older repository direction
- some historical files may still reflect the old anti-scam concept

Manual changes needed:
- decide whether to keep `android-app/` as archive or delete it
- remove unused anti-scam files if they are no longer part of the product
- keep naming consistent across repo, backend, docs, and UI

## 8. Make backend schema and implementation fully consistent
Current state:
- the running app is the tourist-safety MVP
- schema/docs should stay aligned with the current product direction

Manual changes needed:
- keep SQL schema synced with API models
- add database migrations
- keep README, docs, and endpoints consistent after every feature change

## 9. Production-readiness work still needed
Manual changes needed:
- add environment config
- add logging and monitoring
- add rate limiting
- add CORS restrictions
- add audit trails for admins
- add test coverage for edge cases and failures
- add deployment config (Docker, CI/CD, cloud hosting)

## 10. Before presenting or handing over
Recommended checklist:
- confirm the preview runs locally
- test tourist flow end to end
- test admin flow end to end
- generate a fresh zip using `python scripts/create_download_bundle.py`
- share the generated zip from the local `dist/` folder instead of committing the binary to git
