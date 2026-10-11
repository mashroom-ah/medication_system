"""Представления веб-раздела лекарств."""
from django.conf import settings
from django.shortcuts import render

from models.medicines import find_medicine, sort_medicines
from storage import load_medicines


DATA_FILE = settings.BASE_DIR / "data" / "medicines.json"


def medicines(request):
    """Показывает список лекарств и поддерживает поиск по названию."""
    items = load_medicines(str(DATA_FILE))
    query = request.GET.get("q", "").strip()
    if query:
        items = find_medicine(items, query)
    medicines_list = sort_medicines(items)
    context = {
        "medicines": medicines_list,
        "query": query,
    }
    return render(request, "medicines/medicine_list.html", context)


def medicine_detail(request, medicine_id):
    """Показывает лекарство по ID или шаблон ошибки с кодом 404."""
    items = load_medicines(str(DATA_FILE))
    medicine = next(
        (item for item in items if item.id == medicine_id),
        None,
    )
    context = {"medicine": medicine}
    return render(
        request,
        "medicines/medicine_detail.html",
        context,
        status=404 if medicine is None else 200,
    )
