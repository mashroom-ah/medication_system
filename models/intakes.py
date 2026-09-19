from __future__ import annotations

from datetime import date

from .schedules import Schedule


class Intake:
    """Факт приёма лекарства по конкретному расписанию и дате."""

    def __init__(
        self,
        intake_id: int,
        schedule: Schedule,
        intake_date: str,
        taken: bool = True,
    ) -> None:
        """Создаёт запись о приёме лекарства."""
        self.id = intake_id
        self.schedule = schedule
        self.date = intake_date
        self.taken = taken

    def __str__(self) -> str:
        """Возвращает строковое представление записи о приёме."""
        status = "принят" if self.taken else "отменён"
        return (
            f"ID: {self.id}, лекарство: {self.schedule.medicine.name}, "
            f"дата: {self.date}, статус: {status}"
        )

    def cancel(self) -> None:
        """Отменяет запись о приёме, не удаляя её из коллекции."""
        self.taken = False

    @classmethod
    def from_data(
        cls,
        data: dict,
        schedule: Schedule,
    ) -> Intake:
        """Создаёт запись о приёме из данных JSON."""
        return cls(
            intake_id=int(data["id"]),
            schedule=schedule,
            intake_date=str(data["date"]),
            taken=bool(data.get("taken", True)),
        )

    def to_data(self) -> dict:
        """Преобразует запись о приёме в структуру для JSON."""
        return {
            "id": self.id,
            "schedule_id": self.schedule.id,
            "date": self.date,
            "taken": self.taken,
        }


def create_intake(
    intakes: list[Intake],
    schedule: Schedule,
    intake_date: str | None = None,
) -> Intake:
    """Создаёт запись о приёме и добавляет её в коллекцию."""
    if intake_date is None:
        intake_date = date.today().isoformat()
    intake_id = max((intake.id for intake in intakes), default=0) + 1
    intake = Intake(intake_id, schedule, intake_date)
    intakes.append(intake)
    return intake


def is_medicine_taken(
    intakes: list[Intake],
    schedule_id: int,
    intake_date: str,
) -> bool:
    """Проверяет, был ли препарат принят в указанную дату."""
    return any(
        intake.schedule.id == schedule_id
        and intake.date == intake_date
        and intake.taken
        for intake in intakes
    )


def cancel_intake(
    intakes: list[Intake],
    schedule_id: int,
    intake_date: str,
) -> bool:
    """Отменяет запись о приёме, сохраняя её в истории."""
    for intake in intakes:
        if (
            intake.schedule.id == schedule_id
            and intake.date == intake_date
            and intake.taken
        ):
            intake.cancel()
            return True
    return False


def get_intakes_by_date(
    intakes: list[Intake],
    intake_date: str,
) -> list[Intake]:
    """Возвращает записи о приёме за указанную дату."""
    return [intake for intake in intakes if intake.date == intake_date]


def show_intakes(intakes: list[Intake], intake_date: str) -> None:
    """Выводит записи о приёме за указанную дату."""
    daily_intakes = get_intakes_by_date(intakes, intake_date)
    if not daily_intakes:
        print("За эту дату приемов нет.")
        return
    for intake in daily_intakes:
        print(intake)
