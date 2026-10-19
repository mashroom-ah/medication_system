"""Представления каталога лекарств, получающие данные из SQLite."""
from contextlib import closing
from db.database import get_connection
from django.shortcuts import render


def medicines(request):
    """Выводит список лекарств с SQL-поиском и фильтром дозировки."""
    query = request.GET.get("q", "").strip()
    min_dosage_raw = request.GET.get("min_dosage", "").strip()
    min_dosage = None
    if min_dosage_raw:
        try:
            min_dosage = float(min_dosage_raw)
            if min_dosage < 0:
                min_dosage = None
        except ValueError:
            min_dosage = None

    sql = "SELECT id, name, dosage, unit FROM medicines WHERE 1 = 1"
    params = []
    if query:
        sql += " AND name LIKE '%' || ? || '%' COLLATE NOCASE"
        params.append(query)
    if min_dosage is not None:
        sql += " AND dosage >= ?"
        params.append(min_dosage)
    sql += " ORDER BY dosage, name"

    with closing(get_connection()) as connection:
        items = connection.execute(sql, params).fetchall()
    return render(request, "medicines/medicine_list.html", {
        "medicines": items,
        "query": query,
        "min_dosage": min_dosage_raw,
    })


def medicine_detail(request, medicine_id):
    """Показывает лекарство из SQLite либо возвращает страницу со статусом 404."""
    with closing(get_connection()) as connection:
        medicine = connection.execute(
            "SELECT id, name, dosage, unit FROM medicines WHERE id = ?",
            (medicine_id,),
        ).fetchone()
    return render(
        request,
        "medicines/medicine_detail.html",
        {"medicine": medicine},
        status=404 if medicine is None else 200,
    )
