from __future__ import annotations

import json

from models import Intake, Medicine, Schedule, User


def load_data(filename: str) -> list[dict]:
    """Загружает список данных из JSON-файла."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            if not isinstance(data, list):
                raise ValueError("JSON должен содержать список.")
            return data
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def save_data(filename: str, data: list[dict]) -> None:
    """Сохраняет список данных в JSON-файл."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except OSError as error:
        raise OSError(
            f"Не удалось сохранить файл {filename}: {error}"
        ) from error


def load_users(filename: str) -> list[User]:
    """Загружает пользователей и создаёт объекты User."""
    return [User.from_data(item) for item in load_data(filename)]


def save_users(filename: str, users: list[User]) -> None:
    """Сохраняет объекты User в JSON."""
    save_data(filename, [user.to_data() for user in users])


def load_medicines(filename: str) -> list[Medicine]:
    """Загружает лекарства и создаёт объекты Medicine."""
    return [
        Medicine.from_data(item)
        for item in load_data(filename)
    ]


def save_medicines(
    filename: str,
    medicines: list[Medicine],
) -> None:
    """Сохраняет объекты Medicine в JSON."""
    save_data(
        filename,
        [medicine.to_data() for medicine in medicines],
    )


def load_schedules(
    filename: str,
    users: list[User],
    medicines: list[Medicine],
) -> list[Schedule]:
    """Загружает расписания и восстанавливает связи объектов."""
    schedules: list[Schedule] = []
    users_by_id = {user.id: user for user in users}
    medicines_by_id = {
        medicine.id: medicine
        for medicine in medicines
    }
    for item in load_data(filename):
        user = users_by_id.get(int(item["user_id"]))
        medicine = medicines_by_id.get(int(item["medicine_id"]))
        if user is None or medicine is None:
            continue
        schedules.append(
            Schedule.from_data(item, user, medicine)
        )
    return schedules


def save_schedules(
    filename: str,
    schedules: list[Schedule],
) -> None:
    """Сохраняет объекты Schedule в JSON."""
    save_data(
        filename,
        [schedule.to_data() for schedule in schedules],
    )


def load_intakes(
    filename: str,
    schedules: list[Schedule],
) -> list[Intake]:
    """Загружает приёмы и восстанавливает связи с расписаниями."""
    intakes: list[Intake] = []
    schedules_by_id = {
        schedule.id: schedule
        for schedule in schedules
    }
    for item in load_data(filename):
        schedule = schedules_by_id.get(int(item["schedule_id"]))
        if schedule is None:
            continue
        intakes.append(Intake.from_data(item, schedule))
    return intakes


def save_intakes(
    filename: str,
    intakes: list[Intake],
) -> None:
    """Сохраняет объекты Intake в JSON."""
    save_data(filename, [intake.to_data() for intake in intakes])
