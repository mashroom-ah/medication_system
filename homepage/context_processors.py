from medicines.models import Medicine


def room_context(request):
    """Адаптация room_context из методички: общие сведения приложения «Мой приём»."""
    return {
        "app_title": "Мой приём",
        "medicines_count": Medicine.objects.count(),
    }
