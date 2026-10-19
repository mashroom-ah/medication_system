"""Представления расписаний, использующие SQL-запросы к SQLite."""
from contextlib import closing
from datetime import date, datetime

from db.database import get_connection
from django.shortcuts import render


def _schedule_status(hour, minute, taken, now):
    """Рассчитывает текст статуса расписания на текущий день."""
    if taken:
        return "Препарат уже принят."
    scheduled_minutes = hour * 60 + minute
    current_minutes = now.hour * 60 + now.minute
    if current_minutes >= scheduled_minutes:
        return "Необходимо принять препарат."
    return (
        "Время приема еще не наступило. "
        f"Осталось примерно {scheduled_minutes - current_minutes} мин."
    )


def _schedule_from_row(row, now, intake_date):
    """Формирует вложенный контекст, совместимый с существующими шаблонами."""
    return {
        "id": row["id"],
        "hour": row["hour"],
        "minute": row["minute"],
        "user": {"name": row["user_name"]},
        "medicine": {
            "id": row["medicine_id"],
            "name": row["medicine_name"],
            "dosage": row["dosage"],
            "unit": row["unit"],
        },
        "taken": bool(row["taken_today"]),
        "status": _schedule_status(
            row["hour"], row["minute"], bool(row["taken_today"]), now
        ),
    }


def schedules(request):
    """Показывает расписания с названиями лекарств и статусом за сегодня."""
    today = date.today().isoformat()
    now = datetime.now()
    sql = """
        SELECT s.id, s.hour, s.minute, s.medicine_id,
               u.name AS user_name, m.name AS medicine_name, m.dosage, m.unit,
               EXISTS (
                   SELECT 1 FROM intakes AS i
                   WHERE i.schedule_id = s.id AND i.intake_date = ? AND i.taken = 1
               ) AS taken_today
        FROM schedules AS s
        JOIN users AS u ON u.id = s.user_id
        JOIN medicines AS m ON m.id = s.medicine_id
        ORDER BY s.hour, s.minute, s.id
    """
    with closing(get_connection()) as connection:
        rows = connection.execute(sql, (today,)).fetchall()
    schedule_rows = [
        {"schedule": _schedule_from_row(row, now, today),
         "status": _schedule_status(row["hour"], row["minute"],
                                    bool(row["taken_today"]), now)}
        for row in rows
    ]
    return render(request, "schedules/schedule_list.html", {
        "schedule_rows": schedule_rows,
    })


def schedule_detail(request, schedule_id):
    """Показывает одно расписание и вычисленный статус приёма."""
    today = date.today().isoformat()
    now = datetime.now()
    sql = """
        SELECT s.id, s.hour, s.minute, s.medicine_id,
               u.name AS user_name, m.name AS medicine_name, m.dosage, m.unit,
               EXISTS (
                   SELECT 1 FROM intakes AS i
                   WHERE i.schedule_id = s.id AND i.intake_date = ? AND i.taken = 1
               ) AS taken_today
        FROM schedules AS s
        JOIN users AS u ON u.id = s.user_id
        JOIN medicines AS m ON m.id = s.medicine_id
        WHERE s.id = ?
    """
    with closing(get_connection()) as connection:
        row = connection.execute(sql, (today, schedule_id)).fetchone()
    schedule = _schedule_from_row(row, now, today) if row else None
    return render(request, "schedules/schedule_detail.html", {
        "schedule": schedule,
        "status_text": schedule["status"] if schedule else "",
    }, status=404 if schedule is None else 200)
