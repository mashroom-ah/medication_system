from datetime import datetime


def add_schedule(
        schedules: list[dict],
        user_id: int,
        medicine_id: int,
        hour: int,
        minute: int
) -> dict:
    """Добавляет расписание приёма лекарства."""
    schedule_id = len(schedules) + 1

    schedule = {
        "id": schedule_id,
        "user_id": user_id,
        "medicine_id": medicine_id,
        "hour": hour,
        "minute": minute
    }

    schedules.append(schedule)
    return schedule


def is_schedule_due(
        schedule: dict,
        current_time: datetime
) -> bool:
    """Проверяет наступило ли время приёма."""
    scheduled_minutes = schedule["hour"] * 60 + schedule["minute"]
    current_minutes = current_time.hour * 60 + current_time.minute

    return current_minutes >= scheduled_minutes


def get_schedule_status(
        schedule: dict,
        is_taken: bool,
        current_time: datetime
) -> str:
    """Возвращает статус текущего приёма."""
    if is_taken:
        return "Препарат уже принят."

    if is_schedule_due(schedule, current_time):
        return "Время принимать препарат."

    scheduled_minutes = schedule["hour"] * 60 + schedule["minute"]
    current_minutes = current_time.hour * 60 + current_time.minute
    minutes_left = current_minutes - scheduled_minutes

    return (
        "Время ещё не наступило. "
        f"Осталось примерно {minutes_left} мин."
    )


def sort_schedules(schedules: list[dict]):
    return sorted(
        schedules,
        key=lambda schedule: (
            schedule["hour"],
            schedule["minute"]
        )
    )
