from django.contrib import admin

from intakes.models import Intake
from .models import Schedule


class IntakeInline(admin.TabularInline):
    model = Intake
    extra = 0
    fields = ("intake_date", "status")
    ordering = ("-intake_date",)
    show_change_link = True


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user", "medicine", "hour", "minute",
        "total_minutes", "is_night", "intakes_count",
    )
    list_display_links = ("id",)
    list_select_related = ("user", "medicine")
    search_fields = ("user__name", "medicine__name")
    list_filter = ("hour", "minute")
    ordering = ("hour", "minute", "id")
    list_per_page = 20
    inlines = (IntakeInline,)

    @admin.display(description="Записей приёма")
    def intakes_count(self, obj):
        return obj.intakes_count

    def get_queryset(self, request):
        from django.db.models import Count
        return super().get_queryset(request).annotate(intakes_count=Count("intakes"))
