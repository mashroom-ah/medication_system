from django.contrib import admin
from .models import Schedule


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "medicine", "hour", "minute")
    list_select_related = ("user", "medicine")
    list_filter = ("hour",)
