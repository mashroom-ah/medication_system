from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count

from schedules.models import Schedule
from .models import Medicine


class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 0
    fields = ("user", "hour", "minute")
    show_change_link = True


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name", "slug", "dosage", "unit",
        "schedules_count", "public_link",
    )
    list_display_links = ("name",)
    readonly_fields = ("slug", "public_link")
    search_fields = ("name", "unit")
    list_filter = ("unit",)
    ordering = ("name", "dosage", "id")
    list_per_page = 20
    inlines = (ScheduleInline,)

    @admin.display(description="Публичная страница")
    def public_link(self, obj):
        if obj is None or not obj.pk:
            return "Ссылка появится после сохранения"
        return format_html('<a href="{}">Открыть</a>', obj.get_absolute_url())

    @admin.display(description="Расписаний")
    def schedules_count(self, obj):
        return obj.schedules_count

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            schedules_count=Count("schedules")
        )
