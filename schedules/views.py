"""Представления веб-раздела расписаний."""
from datetime import date, datetime

from django.conf import settings
from django.shortcuts import render

from models.intakes import is_medicine_taken
from storage import (
    load_intakes,
    load_medicines,
    load_schedules,
    load_users,
)


DATA_DIR = settings.BASE_DIR / "data"


def _load_schedules():
    """Загружает расписания и восстанавливает связи объектов."""
    users = load_users(str(DATA_DIR / "users.json"))
    medicines = load_medicines(str(DATA_DIR / "medicines.json"))
    return load_schedules(str(DATA_DIR / "schedules.json"), users, medicines)


def _load_intakes(schedules_list):
    """Загружает историю приёмов для переданного списка расписаний."""
    return load_intakes(str(DATA_DIR / "intakes.json"), schedules_list)


def schedules(request):
    """Показывает расписания и текущий статус приёма."""
    items = sorted(_load_schedules(), key=lambda item: (item.hour, item.minute))
    now = datetime.now()
    intakes_list = _load_intakes(items)
    schedule_rows = []
    for item in items:
        taken = is_medicine_taken(
            intakes_list,
            item.id,
            date.today().isoformat(),
        )
        schedule_rows.append({
            "schedule": item,
            "status": item.get_status(taken, now),
        })
    context = {"schedule_rows": schedule_rows}
    return render(request, "schedules/schedule_list.html", context)


def schedule_detail(request, schedule_id):
    """Показывает расписание по ID или возвращает HTTP 404."""
    items = _load_schedules()
    schedule = next(
        (item for item in items if item.id == schedule_id),
        None,
    )
    status_text = ""
    if schedule is not None:
        now = datetime.now()
        intakes_list = _load_intakes(items)
        taken = is_medicine_taken(
            intakes_list,
            schedule.id,
            date.today().isoformat(),
        )
        status_text = schedule.get_status(taken, now)
    context = {
        "schedule": schedule,
        "status_text": status_text,
    }
    return render(
        request,
        "schedules/schedule_detail.html",
        context,
        status=404 if schedule is None else 200,
    )
