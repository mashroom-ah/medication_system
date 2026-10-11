"""Представления веб-раздела истории приёмов."""
from django.conf import settings
from django.shortcuts import render

from storage import load_intakes, load_medicines, load_schedules, load_users


DATA_DIR = settings.BASE_DIR / "data"


def _load_intakes():
    """Загружает историю и связанные объекты из JSON-файлов."""
    users = load_users(str(DATA_DIR / "users.json"))
    medicines = load_medicines(str(DATA_DIR / "medicines.json"))
    schedules = load_schedules(
        str(DATA_DIR / "schedules.json"),
        users,
        medicines,
    )
    return load_intakes(str(DATA_DIR / "intakes.json"), schedules)


def intakes(request):
    """Показывает историю приёмов, отсортированную по дате и ID."""
    items = sorted(
        _load_intakes(),
        key=lambda item: (item.date, item.id),
        reverse=True,
    )
    return render(request, "intakes/intake_list.html", {"intakes": items})


def intake_detail(request, intake_id):
    """Показывает запись о приёме по ID или возвращает HTTP 404."""
    item = next(
        (intake for intake in _load_intakes() if intake.id == intake_id),
        None,
    )
    context = {"intake": item}
    return render(
        request,
        "intakes/intake_detail.html",
        context,
        status=404 if item is None else 200,
    )
