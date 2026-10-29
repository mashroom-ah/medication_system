"""Просмотр расписаний и связанных объектов с использованием Django ORM."""
from datetime import date, datetime

from django.db.models import Count, Exists, OuterRef
from django.shortcuts import render

from intakes.models import Intake
from .models import Schedule


def _status(schedule, taken, now):
    if taken:
        return "Препарат уже принят."
    scheduled_minutes = schedule.hour * 60 + schedule.minute
    current_minutes = now.hour * 60 + now.minute
    if current_minutes >= scheduled_minutes:
        return "Необходимо принять препарат."
    remaining = scheduled_minutes - current_minutes
    return f"Время приема еще не наступило. Осталось примерно {remaining} мин."


def _row(schedule, now, today):
    taken = schedule.intakes.filter(intake_date=today, taken=True).exists()
    return {"schedule": schedule, "status": _status(schedule, taken, now)}


def schedules(request):
    today, now = date.today(), datetime.now()
    taken_today = Intake.objects.filter(
        schedule_id=OuterRef("pk"),
        intake_date=today,
        taken=True,
    )
    queryset = Schedule.objects.select_related("user", "medicine").annotate(
        taken_today=Exists(taken_today),
        intake_count=Count("intakes", distinct=True),
    ).order_by("hour", "minute", "id")
    rows = [
        {"schedule": item, "status": _status(item, item.taken_today, now)}
        for item in queryset
    ]
    return render(request, "schedules/schedule_list.html", {"schedule_rows": rows})


def schedule_detail(request, schedule_id):
    today, now = date.today(), datetime.now()
    schedule = Schedule.objects.select_related(
        "user", "medicine"
    ).filter(pk=schedule_id).first()
    taken = (
        schedule.intakes.filter(intake_date=today, taken=True).exists()
        if schedule else False
    )
    status_text = _status(schedule, taken, now) if schedule else ""
    status = 404 if schedule is None else 200
    return render(
        request,
        "schedules/schedule_detail.html",
        {"schedule": schedule, "status_text": status_text},
        status=status,
    )
