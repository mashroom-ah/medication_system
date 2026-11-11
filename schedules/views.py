"""Просмотр расписаний и связанных объектов с использованием Django ORM."""
from datetime import date, datetime

from django.db.models import Count, Exists, F, OuterRef
from django.shortcuts import get_object_or_404, render

from intakes.models import Intake
from .models import Schedule


def _status(schedule, taken, now):
    if taken:
        return "Препарат уже принят."
    scheduled_minutes = schedule.total_minutes
    current_minutes = now.hour * 60 + now.minute
    if current_minutes >= scheduled_minutes:
        return "Необходимо принять препарат."
    remaining = scheduled_minutes - current_minutes
    return f"Время приема еще не наступило. Осталось примерно {remaining} мин."


def schedules(request):
    today, now = date.today(), datetime.now()
    taken_today = Intake.objects.taken().filter(
        schedule_id=OuterRef("pk"), intake_date=today
    )
    queryset = Schedule.objects.select_related("user", "medicine").annotate(
        taken_today=Exists(taken_today),
        intake_count=Count("intakes", distinct=True),
        computed_minutes=F("hour") * 60 + F("minute"),
    ).order_by("computed_minutes", "id")
    rows = [
        {"schedule": item, "status": _status(item, item.taken_today, now)}
        for item in queryset
    ]
    return render(request, "schedules/schedule_list.html", {"schedule_rows": rows})


def schedule_detail(request, schedule_id):
    today, now = date.today(), datetime.now()
    schedule = get_object_or_404(
        Schedule.objects.select_related("user", "medicine"), pk=schedule_id
    )
    taken = schedule.intakes.taken().for_date(today).exists()
    status_text = _status(schedule, taken, now)
    return render(
        request,
        "schedules/schedule_detail.html",
        {"schedule": schedule, "status_text": status_text},
    )
