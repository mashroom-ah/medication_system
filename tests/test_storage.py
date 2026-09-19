from models.medicines import Medicine
from models.schedules import Schedule
from models.users import User
from storage import (
    load_intakes,
    load_medicines,
    load_schedules,
    load_users,
    save_intakes,
    save_medicines,
    save_schedules,
    save_users,
)
from models.intakes import Intake


def test_json_round_trip(tmp_path) -> None:
    users_file = tmp_path / "users.json"
    medicines_file = tmp_path / "medicines.json"
    schedules_file = tmp_path / "schedules.json"
    intakes_file = tmp_path / "intakes.json"

    users = [User(1, "Мария", 19)]
    medicines = [Medicine(1, "Витамин C", 10, "мг")]
    schedules = [Schedule(1, users[0], medicines[0], 12, 0)]
    intakes = [Intake(1, schedules[0], "2026-09-13", True)]

    save_users(str(users_file), users)
    save_medicines(str(medicines_file), medicines)
    save_schedules(str(schedules_file), schedules)
    save_intakes(str(intakes_file), intakes)

    loaded_users = load_users(str(users_file))
    loaded_medicines = load_medicines(str(medicines_file))
    loaded_schedules = load_schedules(
        str(schedules_file),
        loaded_users,
        loaded_medicines,
    )
    loaded_intakes = load_intakes(str(intakes_file), loaded_schedules)

    assert loaded_users[0].name == "Мария"
    assert loaded_schedules[0].user is loaded_users[0]
    assert loaded_schedules[0].medicine is loaded_medicines[0]
    assert loaded_intakes[0].schedule is loaded_schedules[0]
