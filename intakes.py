from datetime import date


def create_intake(
        intakes: list[dict],
        schedule_id: int,
        intake_date: str | None = None
) -> dict:
    """Создаёт запись о приёме лекарства."""
    if intake_date is None:
        intake_date = date.today().isoformat()

    intake_id = len(intakes) + 1

    intake = {
        "id": intake_id,
        "schedule_id": schedule_id,
        "date": intake_date,
        "is_taken": True
    }

    intakes.append(intake)
    return intake


def is_medicine_taken(
        intakes: list[dict],
        schedule_id: int,
        intake_date: str
) -> bool:
    """Проверяет был ли принят препарат в указанную дату."""
    for intake in intakes:
        if (
            intake["schedule_id"] == schedule_id
            and intake["date"] == intake_date
            and intake["taken"]
        ):
            return True

    return False


def cancel_intake(
        intakes: list[dict],
        schedule_id: int,
        intake_date: str
) -> bool:
    """Отменяет запись о приёме за указанную дату."""
    for intake in intakes:
        if (
            intake["schedule_id"] == schedule_id
            and intake["intake_date"] == intake_date
        ):
            intakes.remove(intake)
            return True

    return False


def get_intakes_by_date(
        intakes: list[dict],
        intake_date: str
) -> list[dict]:
    return [
        intake
        for intake in intakes
        if intake["date"] == intake_date
    ]
