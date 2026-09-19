from __future__ import annotations

from datetime import datetime

from .medicines import Medicine
from .users import User


class Schedule:
    """Расписание приёма лекарства пользователем."""

    def __init__(
        self,
        schedule_id: int,
        user: User,
        medicine: Medicine,
        hour: int,
        minute: int,
    ) -> None:
        """Создаёт расписание и связывает его с пользователем и лекарством."""
        self.id = schedule_id
        self.user = user
        self.medicine = medicine
        self.hour = hour
        self.minute = minute

    def __str__(self) -> str:
        """Возвращает строковое представление расписания."""
        return (
            f"{self.medicine.name} для {self.user.name}, "
            f"время: {self.hour:02d}:{self.minute:02d}, ID: {self.id}"
        )

    @staticmethod
    def validate_time(hour: int, minute: int) -> bool:
        """Проверяет корректность времени приёма."""
        return 0 <= hour <= 23 and 0 <= minute <= 59

    def is_due(self, current_time: datetime) -> bool:
        """Проверяет, наступило ли время приёма."""
        scheduled_minutes = self.hour * 60 + self.minute
        current_minutes = current_time.hour * 60 + current_time.minute
        return current_minutes >= scheduled_minutes

    def get_status(self, is_taken: bool, current_time: datetime) -> str:
        """Возвращает статус текущего приёма."""
        if is_taken:
            return "Препарат уже принят."
        if self.is_due(current_time):
            return "Необходимо принять препарат."
        scheduled_minutes = self.hour * 60 + self.minute
        current_minutes = current_time.hour * 60 + current_time.minute
        minutes_left = scheduled_minutes - current_minutes
        return (
            "Время приема еще не наступило. "
            f"Осталось примерно {minutes_left} мин."
        )

    @classmethod
    def from_data(
        cls,
        data: dict,
        user: User,
        medicine: Medicine,
    ) -> Schedule:
        """Создаёт расписание из данных JSON и связанных объектов."""
        return cls(
            schedule_id=int(data["id"]),
            user=user,
            medicine=medicine,
            hour=int(data["hour"]),
            minute=int(data["minute"]),
        )

    def to_data(self) -> dict:
        """Преобразует расписание в структуру для JSON."""
        return {
            "id": self.id,
            "user_id": self.user.id,
            "medicine_id": self.medicine.id,
            "hour": self.hour,
            "minute": self.minute,
        }


def add_schedule(
    schedules: list[Schedule],
    user: User,
    medicine: Medicine,
    hour: int,
    minute: int,
) -> Schedule:
    """Создаёт расписание и добавляет его в коллекцию."""
    if not Schedule.validate_time(hour, minute):
        raise ValueError("Некорректное время приёма.")
    schedule_id = max(
        (schedule.id for schedule in schedules),
        default=0,
    ) + 1
    schedule = Schedule(
        schedule_id,
        user,
        medicine,
        hour,
        minute,
    )
    schedules.append(schedule)
    return schedule


def sort_schedules(schedules: list[Schedule]) -> list[Schedule]:
    """Сортирует расписания по времени приёма."""
    return sorted(
        schedules,
        key=lambda schedule: (schedule.hour, schedule.minute),
    )


def show_schedules(schedules: list[Schedule]) -> None:
    """Выводит расписания."""
    if not schedules:
        print("Расписаний нет.")
        return
    for schedule in sort_schedules(schedules):
        print(schedule)
