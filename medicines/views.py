"""Каталог лекарств: поиск, фильтрация, сортировка и пагинация через ORM."""
import re
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count, Q
from django.shortcuts import render

from .models import Medicine


def medicines(request):
    query = request.GET.get("q", "").strip()[:100]
    min_dosage_raw = request.GET.get("min_dosage", "").strip()
    min_dosage = None
    if min_dosage_raw:
        try:
            candidate = float(min_dosage_raw)
            if 0 <= candidate < 1e12:
                min_dosage = candidate
        except (ValueError, OverflowError):
            pass

    sort_options = {
        "dosage": "dosage",
        "-dosage": "-dosage",
        "name": "name",
        "-name": "-name",
    }
    sort = request.GET.get("sort", "dosage")
    if sort not in sort_options:
        sort = "dosage"

    queryset = Medicine.objects.annotate(
        schedule_count=Count("schedules", distinct=True)
    )
    if query:
        # SQLite icontains не учитывает регистр кириллицы. iregex использует
        # Unicode-aware case-insensitive matching; экранируем ввод как текст,
        # чтобы пользовательский запрос не интерпретировался как regex.
        escaped_query = re.escape(query)
        queryset = queryset.filter(
            Q(name__iregex=escaped_query) | Q(unit__iregex=escaped_query)
        )
    if min_dosage is not None:
        queryset = queryset.filter(dosage__gte=min_dosage)
    # exclude() используется для исключения некорректных пустых названий.
    queryset = queryset.exclude(name__exact="").order_by(sort_options[sort], "id")

    paginator = Paginator(queryset, 10)
    page_value = request.GET.get("page", "1")
    try:
        page_obj = paginator.page(page_value)
    except (PageNotAnInteger, EmptyPage):
        is_invalid_page = not str(page_value).isdigit() or int(page_value) < 1
        page_number = 1 if is_invalid_page else paginator.num_pages
        page_obj = paginator.page(page_number)

    context = {
        "medicines": page_obj.object_list,
        "page_obj": page_obj,
        "query": query,
        "min_dosage": min_dosage_raw,
        "sort": sort,
    }
    return render(request, "medicines/medicine_list.html", context)


def medicine_detail(request, medicine_id):
    medicine = Medicine.objects.annotate(
        schedule_count=Count("schedules", distinct=True)
    ).filter(pk=medicine_id).first()
    status = 404 if medicine is None else 200
    return render(
        request,
        "medicines/medicine_detail.html",
        {"medicine": medicine},
        status=status,
    )
