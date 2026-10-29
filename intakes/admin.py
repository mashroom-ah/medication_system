from django.contrib import admin
from .models import Intake


@admin.register(Intake)
class IntakeAdmin(admin.ModelAdmin):
    list_display = ("id", "schedule", "intake_date", "taken")
    list_select_related = ("schedule", "schedule__user", "schedule__medicine")
    list_filter = ("taken", "intake_date")
