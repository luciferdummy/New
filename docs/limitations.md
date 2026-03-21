# MVP Limitations and Future Improvements

## 1. Hackathon MVP Limitations

### Data realism limitations
- Crime data will likely be simulated or manually entered by admins.
- Crowd-density, protest, and traffic-risk intelligence will be approximated using seeded data or simplified APIs.
- Hotel, restaurant, and transport reviews will likely come from curated demo content rather than official partner integrations.

### Emergency-response limitations
- No direct integration with real police dispatch, ambulance systems, or national emergency hotlines.
- Response-team assignment will be simulated within the admin dashboard.
- Emergency contact delivery may depend on push notifications rather than guaranteed telecom-grade alerting.

### Navigation and offline limitations
- Fully offline turn-by-turn navigation is difficult to deliver in a short hackathon timeline.
- Safe route quality depends on the map provider and the freshness of unsafe-zone data.
- Background tracking reliability varies by mobile OS battery restrictions.

### Smart detection limitations
- Shake detection, abnormal movement detection, and voice triggers can create false positives.
- Automatic danger detection should not be positioned as a guaranteed emergency detector.
- Offline speech recognition is difficult to implement robustly in a hackathon MVP.

### Security and compliance limitations
- A production-grade document vault requires stronger key management, device binding, and compliance review.
- Real deployments would need clear consent flows, retention policies, and jurisdiction-specific privacy compliance.
- Admin visibility into tourist location data must be limited, auditable, and policy-driven.

## 2. Future Improvements

### Product improvements
- Add verified partner integrations for hotels, transport, and local guides.
- Add embassy and consulate support workflows for foreign travelers.
- Add travel insurance integration and claim-assistance workflows.
- Add multilingual chat assistant for local help and safety guidance.

### Safety improvements
- Connect verified government alert feeds and disaster advisories.
- Add ML-assisted anomaly detection for route risk, scam patterns, and repeated incidents.
- Add wearable trigger support for faster SOS activation.
- Add responder mobile app for field teams.

### Platform improvements
- Use PostGIS for advanced route-risk calculations.
- Add event streaming for large-scale realtime monitoring.
- Add tenant support so different cities or tourism boards can operate independently.
- Add privacy-preserving analytics and automatic data minimization policies.
