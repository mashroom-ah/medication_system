"""Одноразовый/повторяемый перенос исходных JSON-данных в SQLite."""
import json
from pathlib import Path

from db.database import DB_PATH, SCHEMA_PATH, get_connection

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_json(filename: str) -> list[dict]:
    """Читает список записей из JSON-файла."""
    with (DATA_DIR / filename).open(encoding="utf-8") as source:
        data = json.load(source)
    if not isinstance(data, list):
        raise ValueError(f"Ожидался список записей в {filename}")
    return data


def main() -> None:
    """Создаёт схему и атомарно обновляет таблицы данными JSON."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = get_connection()
    try:
        connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        # Удаляем в порядке зависимостей, чтобы повторный импорт не дублировал записи.
        connection.execute("DELETE FROM intakes")
        connection.execute("DELETE FROM schedules")
        connection.execute("DELETE FROM medicines")
        connection.execute("DELETE FROM users")

        users = load_json("users.json")
        medicines = load_json("medicines.json")
        schedules = load_json("schedules.json")
        intakes = load_json("intakes.json")

        connection.executemany(
            "INSERT INTO users (id, name, age) VALUES (?, ?, ?)",
            [(item["id"], item["name"], item["age"]) for item in users],
        )
        connection.executemany(
            "INSERT INTO medicines (id, name, dosage, unit) VALUES (?, ?, ?, ?)",
            [(item["id"], item["name"], item["dosage"], item["unit"])
             for item in medicines],
        )
        connection.executemany(
            "INSERT INTO schedules (id, user_id, medicine_id, hour, minute) "
            "VALUES (?, ?, ?, ?, ?)",
            [(item["id"], item["user_id"], item["medicine_id"],
              item["hour"], item["minute"]) for item in schedules],
        )
        connection.executemany(
            "INSERT INTO intakes (id, schedule_id, intake_date, taken) "
            "VALUES (?, ?, ?, ?)",
            [(item["id"], item["schedule_id"], item["date"], int(item["taken"]))
             for item in intakes],
        )
        connection.commit()
        print(
            "Импорт завершён: "
            f"пользователи={len(users)}, лекарства={len(medicines)}, "
            f"расписания={len(schedules)}, приёмы={len(intakes)}."
        )
        print(f"База данных: {DB_PATH}")
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


if __name__ == "__main__":
    main()
