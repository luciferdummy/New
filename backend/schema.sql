CREATE TABLE users (
    id TEXT PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('tourist', 'admin')),
    password_hash TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE emergency_contacts (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    contact_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    relationship TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE trips (
    id TEXT PRIMARY KEY,
    user_name TEXT NOT NULL,
    city TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    travelers INTEGER NOT NULL,
    interests TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE location_logs (
    id TEXT PRIMARY KEY,
    traveler_name TEXT NOT NULL,
    city TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    panic_mode INTEGER NOT NULL DEFAULT 0,
    recorded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE unsafe_zones (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    city TEXT NOT NULL,
    zone_type TEXT NOT NULL,
    severity INTEGER NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    radius_km REAL NOT NULL,
    advice TEXT NOT NULL,
    active_from TIMESTAMP NOT NULL,
    active_until TIMESTAMP NOT NULL
);

CREATE TABLE incidents (
    id TEXT PRIMARY KEY,
    traveler_name TEXT NOT NULL,
    category TEXT NOT NULL,
    city TEXT NOT NULL,
    description TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    severity INTEGER NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sos_alerts (
    id TEXT PRIMARY KEY,
    traveler_name TEXT NOT NULL,
    city TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    message TEXT NOT NULL,
    trigger_method TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE emergency_services (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    service_type TEXT NOT NULL,
    city TEXT NOT NULL,
    phone TEXT NOT NULL,
    address TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    is_verified INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE notifications (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    audience TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
