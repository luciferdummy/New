# ANTI-SCAM PAYMENT PROTECTION OVERLAY SYSTEM

A hackathon-ready Android + FastAPI MVP that warns users before risky UPI or digital payments by combining SMS analysis, notification monitoring, accessibility-based screen parsing, overlay warnings, local risk heuristics, and backend fraud scoring.

## Repository Structure

```text
android-app/   Android Kotlin + Jetpack Compose app
backend/       FastAPI fraud detection service
docs/          Architecture, data-flow, permissions, walkthrough, and limitations
```

## Key Capabilities

- Accessibility-driven detection of payment screens in apps such as GPay, PhonePe, and Paytm.
- SMS parsing for OTP, debit, credit, scam, and promotion messages.
- Notification listener for collect requests, autopay prompts, and payment alerts.
- On-device risk scoring plus backend fraud analysis.
- Overlay warning with countdown, reasons, and voice warning.
- Transaction logging, known contact tracking, blacklist support, and guardian-mode scaffolding.

## Android App Highlights

- **Dashboard** for system health and permission guidance.
- **Simulation screen** for demoing risky transactions during a hackathon.
- **Risk alert overlay** for high-risk payment screens.
- **History screen** for transaction and alert logs.
- **Settings screen** to explain required permissions and current protection state.
- **Guardian mode** placeholder for notifying a trusted person.

## Backend Highlights

- **FastAPI** fraud scoring API.
- Endpoints:
  - `POST /analyze_transaction`
  - `POST /analyze_message`
  - `POST /risk_score`
  - `GET /blacklist_check/{upi_id}`
  - `GET /health`
- Rule-based scoring using transaction amount, blacklisted UPI IDs, suspicious keywords, timing, receiver familiarity, and collect-request context.

## Quick Start

### Android

1. Open `android-app/` in Android Studio Hedgehog or later.
2. Let Gradle sync and install on a test device.
3. Enable:
   - Accessibility Service
   - Notification Access
   - Draw over other apps
   - SMS permissions
4. Use the **Transaction Simulation** screen for the demo flow.

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Demo Flow

1. Start the backend API.
2. Launch the Android app and grant permissions.
3. Open the simulation screen or a supported payment app.
4. Trigger a transaction with a suspicious amount, new UPI ID, or scam keywords.
5. Watch the overlay show a risk score, reasons, countdown, and spoken warning.

## Important Limitations

- The app **cannot directly intercept or stop bank transactions**.
- The app relies on **Accessibility, SMS, and Notification APIs**, which vary by Android version and OEM policies.
- This is a **warning and decision-support system**, not a guaranteed prevention layer.
- Fraud detection is **rule-based MVP logic** and should be upgraded with richer telemetry and ML for production.
- Some permissions, especially SMS and overlay access, require explicit user trust and can face Play Store policy constraints.

## Documentation

- `docs/architecture.md`
- `docs/demo-walkthrough.md`
- `docs/limitations.md`
