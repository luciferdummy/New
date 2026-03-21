# API Specification

## 1. API Design Goals

The API should support both the tourist mobile app and the admin dashboard while keeping the MVP understandable for judges and easy to build during a hackathon.

Base path example:

```text
/api/v1
```

Authentication:
- Tourist APIs use Bearer JWT.
- Admin APIs use Bearer JWT with role validation.
- Public content endpoints can allow guest access.

## 2. Auth Endpoints

### Tourist auth
- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/refresh`
- `POST /auth/logout`
- `GET /auth/me`

### Admin auth
- `POST /admin/auth/login`
- `POST /admin/auth/refresh`
- `GET /admin/auth/me`

## 3. User and Profile Endpoints

- `GET /users/profile`
- `PATCH /users/profile`
- `GET /users/emergency-contacts`
- `POST /users/emergency-contacts`
- `PATCH /users/emergency-contacts/:id`
- `DELETE /users/emergency-contacts/:id`
- `GET /users/documents`
- `POST /users/documents`
- `DELETE /users/documents/:id`

## 4. Trip Planning Endpoints

- `GET /places?city=&category=&search=`
- `GET /places/:id`
- `GET /places/recommendations?city=`
- `GET /support-services?city=&type=`
- `GET /transport-advice?city=&from=&to=`
- `POST /trips`
- `GET /trips`
- `GET /trips/:id`
- `PATCH /trips/:id`
- `POST /trips/:id/stops`
- `PATCH /trips/:id/stops/:stopId`
- `DELETE /trips/:id/stops/:stopId`

## 5. Safety and Navigation Endpoints

- `POST /location/update`
- `POST /location/check-in`
- `GET /safety/score?lat=&lng=`
- `GET /safety/unsafe-zones?city=`
- `POST /navigation/safe-route`
- `GET /emergency-services/nearby?lat=&lng=&type=`
- `GET /alerts/feed`
- `POST /alerts/acknowledge/:id`

### Example: `POST /navigation/safe-route`

Request body:

```json
{
  "origin": { "lat": 26.9124, "lng": 75.7873 },
  "destination": { "lat": 26.9239, "lng": 75.8267 },
  "travelMode": "driving",
  "avoidRiskAbove": 60,
  "timeOfDay": "night"
}
```

Response body:

```json
{
  "routeId": "rt_123",
  "distanceKm": 6.3,
  "durationMin": 18,
  "safetyScore": 78,
  "warnings": [
    "One segment passes near an admin-flagged protest zone.",
    "Suggested alternate route adds 4 minutes but reduces exposure."
  ],
  "polyline": "encoded_polyline_here"
}
```

## 6. Emergency and Incident Endpoints

- `POST /sos/trigger`
- `POST /sos/:id/cancel`
- `POST /sos/:id/heartbeat`
- `GET /sos/:id/status`
- `POST /incidents`
- `GET /incidents/me`
- `GET /incidents/:id`
- `POST /incidents/:id/messages`

### Example: `POST /sos/trigger`

```json
{
  "tripId": "trip_123",
  "triggerMethod": "button",
  "latitude": 26.9124,
  "longitude": 75.7873,
  "message": "I feel unsafe near the market area"
}
```

## 7. Notification Endpoints

- `GET /notifications`
- `PATCH /notifications/:id/read`
- `POST /notifications/test-push`

## 8. Admin Endpoints

### Live operations
- `GET /admin/dashboard/summary`
- `GET /admin/map/live-tourists`
- `GET /admin/map/active-sos`
- `GET /admin/incidents`
- `GET /admin/incidents/:id`
- `PATCH /admin/incidents/:id/status`
- `POST /admin/incidents/:id/assign`
- `POST /admin/incidents/:id/respond`
- `GET /admin/sos`
- `PATCH /admin/sos/:id/status`

### Unsafe zones and alerts
- `GET /admin/unsafe-zones`
- `POST /admin/unsafe-zones`
- `PATCH /admin/unsafe-zones/:id`
- `DELETE /admin/unsafe-zones/:id`
- `POST /admin/broadcasts`
- `GET /admin/broadcasts`

### Content management
- `POST /admin/places`
- `PATCH /admin/places/:id`
- `DELETE /admin/places/:id`
- `POST /admin/emergency-services`
- `PATCH /admin/emergency-services/:id`

### Analytics and governance
- `GET /admin/analytics/incidents?from=&to=&city=`
- `GET /admin/analytics/heatmap?from=&to=&city=`
- `GET /admin/users`
- `PATCH /admin/users/:id/status`
- `GET /admin/audit-logs`

## 9. Realtime Events

Recommended WebSocket channels:
- `tourist.alerts.{userId}`
- `tourist.sos.{userId}`
- `admin.ops.global`
- `admin.case.{caseId}`

Event types:
- `zone_alert_created`
- `sos_triggered`
- `sos_acknowledged`
- `incident_created`
- `incident_status_changed`
- `broadcast_sent`
- `checkin_missed`

## 10. Validation and Security Rules

- Rate limit location updates and SOS retry attempts.
- Do not allow admins to access documents unless explicitly designed and audited.
- Require audit logs for zone changes, user suspensions, and incident-status updates.
- Encrypt document metadata references and store binary files outside the relational database.
- Mask contact details in analytics exports.
