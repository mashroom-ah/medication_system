from django.conf import settings
from django.http import HttpResponse

from homepage.views import page
from storage import load_intakes, load_medicines, load_schedules, load_users

DATA_DIR = settings.BASE_DIR / "data"


def _load_intakes():
    users = load_users(str(DATA_DIR / "users.json"))
    medicines = load_medicines(str(DATA_DIR / "medicines.json"))
    schedules = load_schedules(str(DATA_DIR / "schedules.json"), users, medicines)
    return load_intakes(str(DATA_DIR / "intakes.json"), schedules)


def intakes(request):
    """Показывает историю приёмов, сохранённую в JSON."""
    items = sorted(_load_intakes(), key=lambda item: (item.date, item.id), reverse=True)
    rows = ""
    for item in items:
        status = "Принят" if item.taken else "Отменён"
        badge = "bg-success" if item.taken else "bg-secondary"
        rows += f'''<li class="list-group-item d-flex justify-content-between">
            <a href="/intakes/{item.id}/">{item.schedule.medicine.name} — {item.date}</a>
            <span class="badge {badge}">{status}</span>
        </li>'''
    if not rows:
        rows = '<li class="list-group-item">Записей о приёме пока нет.</li>'
    content = f'<h1 class="mb-3">История приёмов</h1><ul class="list-group">{rows}</ul>'
    return HttpResponse(page("Мой приём — история приёмов", content))


def intake_detail(request, intake_id):
    """Показывает отдельную запись истории приёма."""
    item = next((intake for intake in _load_intakes() if intake.id == intake_id), None)
    if item is None:
        content = '''<h1 class="text-danger">Запись не найдена</h1>
        <a class="btn btn-outline-secondary" href="/intakes/">К истории приёмов</a>'''
        return HttpResponse(page("Запись не найдена", content), status=404)

    status = "Принят" if item.taken else "Отменён"
    content = f'''
    <div class="card shadow-sm"><div class="card-body">
        <h1 class="card-title">Запись о приёме №{item.id}</h1>
        <p><strong>Лекарство:</strong> {item.schedule.medicine.name}</p>
        <p><strong>Пользователь:</strong> {item.schedule.user.name}</p>
        <p><strong>Дата:</strong> {item.date}</p>
        <p><strong>Время по расписанию:</strong>
            {item.schedule.hour:02d}:{item.schedule.minute:02d}</p>
        <p><strong>Статус:</strong> {status}</p>
        <a class="btn btn-outline-secondary" href="/intakes/">К истории приёмов</a>
    </div></div>'''
    return HttpResponse(page(f"Запись о приёме №{item.id}", content))
