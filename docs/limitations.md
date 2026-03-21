# MVP Limitations and Future Improvements

## Current Limitations

- The app cannot directly access bank or UPI network APIs.
- The app cannot stop an already-submitted payment at the settlement layer.
- Accessibility is used only to read visible on-screen details.
- Notification and SMS monitoring can be restricted by OEM policies and newer Android versions.
- The backend uses rule-based scoring; it is not a production-trained machine learning model.
- Extensive permissions may reduce user adoption and require strong privacy messaging.
- Google Play distribution may require additional compliance for SMS and accessibility usage.

## Future Improvements

- Add on-device ML anomaly detection for personalized spending behavior.
- Integrate threat intelligence feeds for live blacklist updates.
- Add guardian push notifications and emergency phone-call workflows.
- Introduce secure biometric confirmation for risky overrides.
- Add multilingual voice warnings and larger accessibility presets.
- Add federated analytics to improve scam detection without centralizing raw personal data.
