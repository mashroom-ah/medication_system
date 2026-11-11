"""История фактических приёмов: ORM, фильтрация дат, поиск и пагинация."""
import re
from datetime import date

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from homepage.models import User
from medicines.models import Medicine
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
    user_id = request.GET.get("user", "")
    medicine_id = request.GET.get("medicine", "")
    sort_options = {
        "-date": "-intake_date",
        "date": "intake_date",
        "user": "schedule__user__name",
        "medicine": "schedule__medicine__name",
    }
    sort = request.GET.get("sort", "-date")
    if sort not in sort_options:
        sort = "-date"
    queryset = Intake.objects.select_related("schedule__user", "schedule__medicine")
    if intake_date:
        queryset = queryset.for_date(intake_date)
    if user_id.isdigit() and int(user_id) > 0:
        queryset = queryset.filter(schedule__user_id=int(user_id))
    else:
        user_id = ""
    if medicine_id.isdigit() and int(medicine_id) > 0:
        queryset = queryset.filter(schedule__medicine_id=int(medicine_id))
    else:
        medicine_id = ""
    if query:
        escaped_query = re.escape(query)
        queryset = queryset.filter(
            Q(schedule__medicine__name__iregex=escaped_query)
            | Q(schedule__user__name__iregex=escaped_query)
        )
    if status == Intake.Status.TAKEN:
        queryset = queryset.taken()
    elif status == Intake.Status.MISSED:
        queryset = queryset.missed()
    elif status == Intake.Status.SKIPPED:
        queryset = queryset.skipped()
    queryset = queryset.order_by(sort_options[sort], "-id")
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
        "user_id": user_id,
        "medicine_id": medicine_id,
        "sort": sort,
        "users": User.objects.order_by("name"),
        "medicines": Medicine.objects.order_by("name"),
    }
    return render(request, "intakes/intake_list.html", context)


def intake_detail(request, intake_id):
    item = get_object_or_404(
        Intake.objects.select_related("schedule__user", "schedule__medicine"),
        pk=intake_id,
    )
    return render(request, "intakes/intake_detail.html", {"intake": item})
