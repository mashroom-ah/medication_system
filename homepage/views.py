"""Главная страница и статистика, рассчитанная средствами Django ORM."""
from django.db.models import Avg, Count, Max, Min, Q
from django.shortcuts import render

from intakes.models import Intake
from medicines.models import Medicine
from schedules.models import Schedule
from .models import User


def index(request):
    return render(request, "homepage/index.html")


def statistics(request):
    totals = {
        "users_count": User.objects.count(),
        "medicines_count": Medicine.objects.count(),
        "schedules_count": Schedule.objects.count(),
        "intakes_count": Intake.objects.count(),
    }
    medicine_stats = Medicine.objects.annotate(
        schedules_count=Count("schedules", distinct=True),
        intakes_count=Count("schedules__intakes", distinct=True),
    ).values("name", "schedules_count", "intakes_count").order_by(
        "-schedules_count", "name"
    )
    status_stats = Intake.objects.values("status").annotate(
        records_count=Count("id")
    ).order_by("status")
    intake_metrics = Intake.objects.aggregate(
        earliest_date=Min("intake_date"),
        latest_date=Max("intake_date"),
        completed_count=Count("id", filter=Q(status=Intake.Status.TAKEN)),
    )
    intake_metrics["average_per_schedule"] = Schedule.objects.annotate(
        records=Count("intakes")
    ).aggregate(value=Avg("records"))["value"]
    return render(request, "homepage/statistics.html", {
        "totals": totals,
        "medicine_stats": medicine_stats,
        "status_stats": status_stats,
        "intake_metrics": intake_metrics,
    })


def page_not_found(request, exception):
    return render(request, "404.html", status=404)
