"""Представления истории приёмов, получающие данные из SQLite."""
from contextlib import closing
from db.database import get_connection
from django.shortcuts import render


def _intake_context(row):
    """Преобразует строку JOIN в структуру для существующих шаблонов DTL."""
    return {
        "id": row["id"],
        "date": row["intake_date"],
        "taken": bool(row["taken"]),
        "schedule": {
            "id": row["schedule_id"],
            "hour": row["hour"],
            "minute": row["minute"],
            "user": {"name": row["user_name"]},
            "medicine": {
                "name": row["medicine_name"],
                "dosage": row["dosage"],
                "unit": row["unit"],
            },
        },
    }


def intakes(request):
    """Показывает историю; необязательный параметр date фильтрует по дате."""
    intake_date = request.GET.get("date", "").strip()
    sql = """
        SELECT i.id, i.schedule_id, i.intake_date, i.taken,
               s.hour, s.minute, u.name AS user_name,
               m.name AS medicine_name, m.dosage, m.unit
        FROM intakes AS i
        JOIN schedules AS s ON s.id = i.schedule_id
        JOIN users AS u ON u.id = s.user_id
        JOIN medicines AS m ON m.id = s.medicine_id
    """
    params = []
    if intake_date:
        sql += " WHERE i.intake_date = ?"
        params.append(intake_date)
    sql += " ORDER BY i.intake_date DESC, i.id DESC"
    with closing(get_connection()) as connection:
        rows = connection.execute(sql, params).fetchall()
    items = [_intake_context(row) for row in rows]
    return render(request, "intakes/intake_list.html", {
        "intakes": items,
        "intake_date": intake_date,
    })


def intake_detail(request, intake_id):
    """Показывает запись о приёме по ID или возвращает HTTP 404."""
    sql = """
        SELECT i.id, i.schedule_id, i.intake_date, i.taken,
               s.hour, s.minute, u.name AS user_name,
               m.name AS medicine_name, m.dosage, m.unit
        FROM intakes AS i
        JOIN schedules AS s ON s.id = i.schedule_id
        JOIN users AS u ON u.id = s.user_id
        JOIN medicines AS m ON m.id = s.medicine_id
        WHERE i.id = ?
    """
    with closing(get_connection()) as connection:
        row = connection.execute(sql, (intake_id,)).fetchone()
    item = _intake_context(row) if row else None
    return render(request, "intakes/intake_detail.html", {
        "intake": item,
    }, status=404 if item is None else 200)
