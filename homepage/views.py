from django.http import HttpResponse


def page(title: str, content: str) -> str:
    """Собирает общий HTML-каркас страницы с Bootstrap и навигацией."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f'''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body class="bg-light">
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary mb-4">
        <div class="container">
            <a class="navbar-brand" href="/">Мой приём</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/medicines/">Лекарства</a>
                <a class="nav-link" href="/schedules/">Расписание</a>
                <a class="nav-link" href="/intakes/">История приёмов</a>
            </div>
        </div>
    </nav>
    <main class="container pb-5">{content}</main>
</body>
</html>'''


def index(request):
    content = """
    <div class="p-4 p-md-5 mb-4 bg-white rounded-3 shadow-sm">
        <h1 class="display-5">Мой приём</h1>
        <p class="lead">Учёт лекарств и расписания приёма препаратов.</p>
        <p>Веб-интерфейс использует существующие классы предметной области
        и данные из JSON-файлов проекта.</p>
        <a href="/medicines/" class="btn btn-primary me-2">Лекарства</a>
        <a href="/schedules/" class="btn btn-outline-primary me-2">Расписание</a>
        <a href="/intakes/" class="btn btn-outline-secondary">История приёмов</a>
    </div>
    """
    return HttpResponse(page("Мой приём — главная", content))


def page_not_found(request, exception):
    content = """
    <h1 class="text-danger">404 — страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную страницу.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(page("404 — страница не найдена", content), status=404)
