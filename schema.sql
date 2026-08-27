PRAGMA foreign_keys = ON;

CREATE TABLE rovers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    battery_consumption REAL NOT NULL,
    max_speed REAL NOT NULL,
    max_acceleration REAL NOT NULL,
    max_turn_rate REAL NOT NULL
);

CREATE TABLE missions (
    id INTEGER PRIMARY KEY,
    rover_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    duration REAL NOT NULL,
    result TEXT,
    FOREIGN KEY (rover_id) REFERENCES rovers(id)
);

CREATE TABLE telemetry (
    id INTEGER PRIMARY KEY,
    mission_id INTEGER NOT NULL,
    time REAL NOT NULL,
    position_x REAL NOT NULL,
    position_y REAL NOT NULL,
    position_z REAL NOT NULL,
    heading REAL NOT NULL,
    speed REAL NOT NULL,
    battery REAL NOT NULL,
    operational INTEGER NOT NULL,
    FOREIGN KEY (mission_id) REFERENCES missions(id)
);