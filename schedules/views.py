from datetime import date, datetime

from django.conf import settings
from django.http import HttpResponse

from homepage.views import page
from models.intakes import is_medicine_taken
from storage import (
    load_intakes,
    load_medicines,
    load_schedules,
    load_users,
)

DATA_DIR = settings.BASE_DIR / "data"


def _load_schedules():
    users = load_users(str(DATA_DIR / "users.json"))
    medicines = load_medicines(str(DATA_DIR / "medicines.json"))
    return load_schedules(str(DATA_DIR / "schedules.json"), users, medicines)


def _load_intakes(schedules_list):
    return load_intakes(str(DATA_DIR / "intakes.json"), schedules_list)


def schedules(request):
    """Показывает расписания и статус приёма на текущий момент."""
    items = sorted(_load_schedules(), key=lambda item: (item.hour, item.minute))
    now = datetime.now()
    intakes_list = _load_intakes(items)
    rows = ""
    for item in items:
        taken = is_medicine_taken(
            intakes_list, item.id, date.today().isoformat()
        )
        status = item.get_status(taken, now)
        rows += f'''<li class="list-group-item d-flex justify-content-between">
            <a href="/schedules/{item.id}/">{item.medicine.name}</a>
            <span>{item.hour:02d}:{item.minute:02d} — {status}</span>
        </li>'''
    if not rows:
        rows = '<li class="list-group-item">Расписаний пока нет.</li>'
    content = f'<h1 class="mb-3">Расписание приёма</h1><ul class="list-group">{rows}</ul>'
    return HttpResponse(page("Мой приём — расписание", content))


def schedule_detail(request, schedule_id):
    """Показывает расписание по идентификатору."""
    items = _load_schedules()
    item = next((schedule for schedule in items if schedule.id == schedule_id), None)
    if item is None:
        content = '''<h1 class="text-danger">Расписание не найдено</h1>
        <a class="btn btn-outline-secondary" href="/schedules/">К расписанию</a>'''
        return HttpResponse(page("Расписание не найдено", content), status=404)

    now = datetime.now()
    intakes_list = _load_intakes(items)
    taken = is_medicine_taken(
        intakes_list, item.id, date.today().isoformat()
    )
    content = f'''
    <div class="card shadow-sm"><div class="card-body">
        <h1 class="card-title">{item.medicine.name}</h1>
        <p><strong>ID расписания:</strong> {item.id}</p>
        <p><strong>Пользователь:</strong> {item.user.name}</p>
        <p><strong>Лекарство:</strong> {item.medicine.name}</p>
        <p><strong>Время:</strong> {item.hour:02d}:{item.minute:02d}</p>
        <p><strong>Статус:</strong> {item.get_status(taken, now)}</p>
        <a class="btn btn-outline-secondary" href="/schedules/">К расписанию</a>
    </div></div>'''
    return HttpResponse(page(f"Расписание №{item.id}", content))
