"""Представления главной страницы, статистики и страницы ошибки."""
from contextlib import closing
from db.database import get_connection
from django.shortcuts import render


def index(request):
    """Отображает главную страницу проекта."""
    return render(request, "homepage/index.html")


def statistics(request):
    """Показывает SQL-статистику по лекарствам, расписаниям и истории приёмов."""
    with closing(get_connection()) as connection:
        totals = connection.execute("""
            SELECT (SELECT COUNT(*) FROM users) AS users_count,
                   (SELECT COUNT(*) FROM medicines) AS medicines_count,
                   (SELECT COUNT(*) FROM schedules) AS schedules_count,
                   (SELECT COUNT(*) FROM intakes) AS intakes_count
        """).fetchone()
        medicine_stats = connection.execute("""
            SELECT m.id, m.name, COUNT(DISTINCT s.id) AS schedules_count,
                   COUNT(DISTINCT i.id) AS intakes_count
            FROM medicines AS m
            LEFT JOIN schedules AS s ON s.medicine_id = m.id
            LEFT JOIN intakes AS i ON i.schedule_id = s.id
            GROUP BY m.id, m.name
            ORDER BY schedules_count DESC, m.name
        """).fetchall()
        status_stats = connection.execute("""
            SELECT taken, COUNT(*) AS records_count
            FROM intakes GROUP BY taken ORDER BY taken DESC
        """).fetchall()
    return render(request, "homepage/statistics.html", {
        "totals": totals,
        "medicine_stats": medicine_stats,
        "status_stats": status_stats,
    })


def page_not_found(request, exception):
    """Возвращает пользовательскую страницу с HTTP-статусом 404."""
    return render(request, "404.html", status=404)
