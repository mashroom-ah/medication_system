"""Представления главной страницы и общей страницы ошибки."""
from django.shortcuts import render


def index(request):
    """Отображает главную страницу проекта."""
    return render(request, "homepage/index.html")


def page_not_found(request, exception):
    """Возвращает пользовательскую страницу с HTTP-статусом 404."""
    return render(request, "404.html", status=404)
