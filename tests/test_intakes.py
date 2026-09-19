from models.intakes import (
    Intake,
    cancel_intake,
    create_intake,
    get_intakes_by_date,
    is_medicine_taken,
)
from models.medicines import Medicine
from models.schedules import Schedule
from models.users import User


def make_schedule() -> Schedule:
    return Schedule(
        1,
        User(1, "Мария", 19),
        Medicine(1, "Витамин C", 10, "мг"),
        12,
        0,
    )


def test_create_intake() -> None:
    intakes: list[Intake] = []
    intake = create_intake(intakes, make_schedule(), "2026-09-13")
    assert intake.id == 1
    assert intake.taken is True
    assert intake.schedule.id == 1


def test_is_medicine_taken_for_date() -> None:
    schedule = make_schedule()
    intakes = [Intake(1, schedule, "2026-09-13", True)]
    assert is_medicine_taken(intakes, 1, "2026-09-13")
    assert not is_medicine_taken(intakes, 1, "2026-09-14")


def test_cancel_intake_keeps_object() -> None:
    schedule = make_schedule()
    intake = Intake(1, schedule, "2026-09-13", True)
    intakes = [intake]
    assert cancel_intake(intakes, 1, "2026-09-13")
    assert intakes == [intake]
    assert intake.taken is False


def test_get_intakes_by_date() -> None:
    schedule = make_schedule()
    intakes = [
        Intake(1, schedule, "2026-09-13", True),
        Intake(2, schedule, "2026-09-14", True),
    ]
    result = get_intakes_by_date(intakes, "2026-09-13")
    assert len(result) == 1
    assert result[0].id == 1
