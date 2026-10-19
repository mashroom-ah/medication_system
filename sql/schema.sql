-- «Мой приём»: схема реляционной базы данных SQLite.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL CHECK (age BETWEEN 1 AND 120)
);

CREATE TABLE IF NOT EXISTS medicines (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    dosage REAL NOT NULL CHECK (dosage > 0),
    unit TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS schedules (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    medicine_id INTEGER NOT NULL,
    hour INTEGER NOT NULL CHECK (hour BETWEEN 0 AND 23),
    minute INTEGER NOT NULL CHECK (minute BETWEEN 0 AND 59),
    FOREIGN KEY (user_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (medicine_id) REFERENCES medicines(id) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS intakes (
    id INTEGER PRIMARY KEY,
    schedule_id INTEGER NOT NULL,
    intake_date TEXT NOT NULL CHECK (length(intake_date) = 10),
    taken INTEGER NOT NULL DEFAULT 1 CHECK (taken IN (0, 1)),
    FOREIGN KEY (schedule_id) REFERENCES schedules(id) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_medicines_name ON medicines(name);
CREATE INDEX IF NOT EXISTS idx_schedules_user_time ON schedules(user_id, hour, minute);
CREATE INDEX IF NOT EXISTS idx_intakes_date ON intakes(intake_date);
CREATE INDEX IF NOT EXISTS idx_intakes_schedule_date ON intakes(schedule_id, intake_date);
