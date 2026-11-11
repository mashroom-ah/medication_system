from django.contrib import admin

from .models import Intake


@admin.register(Intake)
class IntakeAdmin(admin.ModelAdmin):
    list_display = (
        "id", "schedule", "user_name", "medicine_name",
        "intake_date", "status",
    )
    list_display_links = ("id",)
    list_select_related = ("schedule", "schedule__user", "schedule__medicine")
    search_fields = ("schedule__user__name", "schedule__medicine__name")
    list_filter = ("status", "intake_date")
    ordering = ("-intake_date", "-id")
    list_per_page = 25

    @admin.display(description="Пользователь", ordering="schedule__user__name")
    def user_name(self, obj):
        return obj.schedule.user.name

    @admin.display(description="Лекарство", ordering="schedule__medicine__name")
    def medicine_name(self, obj):
        return obj.schedule.medicine.name
