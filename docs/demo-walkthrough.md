# Demo Walkthrough

## Installation Steps

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Android App

1. Open `android-app` in Android Studio.
2. Connect an Android device or emulator running Android 8.0+.
3. Update the API base URL if needed in `BuildConfig.API_BASE_URL`.
4. Install and run the app.
5. Grant SMS, overlay, notification, and accessibility permissions.

## Hackathon Demo Script

1. Start on the **Dashboard** screen and explain the live protection layers.
2. Open **Settings** and show why each permission exists.
3. Open **Transaction Simulation**.
4. Trigger the high-risk simulation:
   - unknown receiver
   - blacklisted UPI ID
   - urgent refund message
   - short link
   - OTP context
   - collect request
5. Show the **History** screen updating with the logged risk event.
6. Explain that on a real device, accessibility and notification listeners feed the same engine.
7. Highlight that the overlay gives the user one last safety checkpoint before proceeding.

## Judge-Friendly Talking Points

- Built for elderly users and first-time digital payment users.
- High-contrast UI and voice warnings improve accessibility.
- Transparent rule-based risk scoring keeps alerts explainable.
- Backend API enables future integration with live fraud intelligence feeds.
- Guardian mode opens a path for family-assisted fraud prevention.
