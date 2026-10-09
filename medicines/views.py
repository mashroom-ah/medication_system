from django.conf import settings
from django.http import HttpResponse
from django.utils.html import escape

from homepage.views import page
from models.medicines import (
    find_medicine,
    sort_medicines,
)
from storage import load_medicines


DATA_FILE = settings.BASE_DIR / "data" / "medicines.json"


def medicines(request):
    """Показывает список лекарств, используя JSON-хранилище ПР3."""
    items = load_medicines(str(DATA_FILE))
    query = request.GET.get("q", "").strip()
    if query:
        items = find_medicine(items, query)
    items = sort_medicines(items)
    query_html = escape(query)

    rows = ""
    for medicine in items:
        rows += f'''<li class="list-group-item d-flex justify-content-between">
            <a href="/medicines/{medicine.id}/">{medicine.name}</a>
            <span>{medicine.dosage} {medicine.unit}</span>
        </li>'''
    if not rows:
        rows = '<li class="list-group-item">Лекарства не найдены.</li>'
    content = f'''
    <h1 class="mb-3">Лекарства</h1>
    <form method="get" class="row g-2 mb-3">
        <div class="col-sm-8">
            <input class="form-control" type="search" name="q"
                   placeholder="Поиск по названию" value="{query_html}">
        </div>
        <div class="col-auto"><button class="btn btn-primary">Найти</button></div>
    </form>
    <ul class="list-group">{rows}</ul>'''
    return HttpResponse(page("Мой приём — лекарства", content))


def medicine_detail(request, medicine_id):
    """Показывает карточку лекарства или ответ 404."""
    items = load_medicines(str(DATA_FILE))
    medicine = next((item for item in items if item.id == medicine_id), None)
    if medicine is None:
        content = '''<h1 class="text-danger">Лекарство не найдено</h1>
        <a class="btn btn-outline-secondary" href="/medicines/">К списку лекарств</a>'''
        return HttpResponse(page("Лекарство не найдено", content), status=404)

    content = f'''
    <div class="card shadow-sm"><div class="card-body">
        <h1 class="card-title">{medicine.name}</h1>
        <p><strong>ID:</strong> {medicine.id}</p>
        <p><strong>Дозировка:</strong> {medicine.dosage} {medicine.unit}</p>
        <a class="btn btn-outline-secondary" href="/medicines/">К списку лекарств</a>
    </div></div>'''
    return HttpResponse(page(medicine.name, content))
