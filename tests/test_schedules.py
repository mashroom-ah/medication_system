from datetime import datetime

from models.medicines import Medicine
from models.schedules import Schedule, add_schedule, sort_schedules
from models.users import User


def make_schedule() -> Schedule:
    return Schedule(
        1,
        User(1, "Мария", 19),
        Medicine(1, "Витамин C", 10, "мг"),
        12,
        0,
    )


def test_schedule_links_objects() -> None:
    schedule = make_schedule()
    assert isinstance(schedule.user, User)
    assert isinstance(schedule.medicine, Medicine)
    assert schedule.medicine.name == "Витамин C"


def test_add_schedule() -> None:
    schedules: list[Schedule] = []
    schedule = add_schedule(
        schedules,
        User(1, "Мария", 19),
        Medicine(1, "Витамин C", 10, "мг"),
        12,
        0,
    )
    assert schedule.id == 1
    assert schedules == [schedule]


def test_schedule_due_and_status() -> None:
    schedule = make_schedule()
    assert schedule.is_due(datetime(2026, 9, 13, 12, 30))
    assert not schedule.is_due(datetime(2026, 9, 13, 11, 30))
    assert schedule.get_status(
        True,
        datetime(2026, 9, 13, 12, 30),
    ) == "Препарат уже принят."


def test_sort_schedules() -> None:
    first = make_schedule()
    second = Schedule(
        2,
        first.user,
        first.medicine,
        9,
        30,
    )
    result = sort_schedules([first, second])
    assert result[0].hour == 9
