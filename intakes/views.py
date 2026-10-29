"""История фактических приёмов: ORM, фильтрация дат, поиск и пагинация."""
from datetime import date

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.shortcuts import render

from .models import Intake


def intakes(request):
    date_raw = request.GET.get("date", "").strip()
    intake_date = None
    date_error = False
    if date_raw:
        try:
            intake_date = date.fromisoformat(date_raw)
            if intake_date.isoformat() != date_raw:
                raise ValueError
        except ValueError:
            date_error = True
            date_raw = ""

    query = request.GET.get("q", "").strip()[:100]
    status = request.GET.get("status", "")
    queryset = Intake.objects.select_related("schedule__user", "schedule__medicine")
    if intake_date:
        queryset = queryset.filter(intake_date=intake_date)
    if query:
        queryset = queryset.filter(
            Q(schedule__medicine__name__icontains=query)
            | Q(schedule__user__name__icontains=query)
        )
    if status in ("taken", "missed"):
        queryset = queryset.filter(taken=(status == "taken"))
    queryset = queryset.order_by("-intake_date", "-id")
    paginator = Paginator(queryset, 10)
    page_value = request.GET.get("page", "1")
    try:
        page_obj = paginator.page(page_value)
    except (PageNotAnInteger, EmptyPage):
        is_invalid_page = not str(page_value).isdigit() or int(page_value) < 1
        page_number = 1 if is_invalid_page else max(paginator.num_pages, 1)
        page_obj = paginator.page(page_number)

    context = {
        "intakes": page_obj.object_list,
        "page_obj": page_obj,
        "intake_date": date_raw,
        "date_error": date_error,
        "query": query,
        "status": status,
    }
    return render(request, "intakes/intake_list.html", context)


def intake_detail(request, intake_id):
    item = Intake.objects.select_related(
        "schedule__user", "schedule__medicine"
    ).filter(pk=intake_id).first()
    status = 404 if item is None else 200
    return render(
        request,
        "intakes/intake_detail.html",
        {"intake": item},
        status=status,
    )
