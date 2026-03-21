CREATE TABLE transaction_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    receiver TEXT NOT NULL,
    upi_id TEXT NOT NULL,
    amount REAL NOT NULL,
    source TEXT NOT NULL,
    risk_score INTEGER NOT NULL,
    risk_level TEXT NOT NULL,
    reasons TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE known_contacts (
    upi_id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    last_seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE blacklisted_upi_ids (
    upi_id TEXT PRIMARY KEY,
    reason TEXT NOT NULL
);

CREATE TABLE scam_keywords (
    keyword TEXT PRIMARY KEY,
    severity INTEGER NOT NULL DEFAULT 10
);

CREATE TABLE risk_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    payload_summary TEXT NOT NULL,
    risk_score INTEGER NOT NULL,
    reasons TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
