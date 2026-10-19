"""Проверки схемы SQLite и переноса исходных JSON-данных."""
import sqlite3
from contextlib import closing

from db.database import DB_PATH, SCHEMA_PATH, get_connection


def test_schema_has_expected_tables_and_foreign_keys():
    connection = sqlite3.connect(":memory:")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    tables = {
        row[0] for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        )
    }
    assert {"users", "medicines", "schedules", "intakes"} <= tables
    assert len(connection.execute("PRAGMA foreign_key_list(schedules)").fetchall()) == 2
    assert len(connection.execute("PRAGMA foreign_key_list(intakes)").fetchall()) == 1
    connection.close()


def test_imported_database_has_records_and_join_results():
    assert DB_PATH.exists(), "Сначала выполните python -m db.import_json"
    with closing(get_connection()) as connection:
        assert connection.execute("SELECT COUNT(*) FROM users").fetchone()[0] >= 1
        assert connection.execute("SELECT COUNT(*) FROM medicines").fetchone()[0] >= 1
        rows = connection.execute("""
            SELECT i.id, m.name AS medicine_name, u.name AS user_name
            FROM intakes AS i
            JOIN schedules AS s ON s.id = i.schedule_id
            JOIN medicines AS m ON m.id = s.medicine_id
            JOIN users AS u ON u.id = s.user_id
        """).fetchall()
        assert rows
        assert rows[0]["medicine_name"]
        assert rows[0]["user_name"]


def test_parameterized_medicine_search():
    with closing(get_connection()) as connection:
        rows = connection.execute(
            "SELECT name FROM medicines WHERE name LIKE ?", ("%Аскорбиновая%",)
        ).fetchall()
    assert rows
