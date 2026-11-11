from django.contrib import admin

from .models import User
from schedules.models import Schedule

admin.site.site_header = "Администрирование системы «Мой приём»"
admin.site.site_title = "Мой приём — администрирование"
admin.site.index_title = "Управление данными приложения"


class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 0
    fields = ("medicine", "hour", "minute")
    show_change_link = True


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "age", "schedules_count")
    list_display_links = ("name",)
    search_fields = ("name",)
    list_filter = ("age",)
    ordering = ("name", "id")
    list_per_page = 20
    inlines = (ScheduleInline,)

    @admin.display(description="Расписаний")
    def schedules_count(self, obj):
        return obj.schedules_count

    def get_queryset(self, request):
        from django.db.models import Count
        return super().get_queryset(request).annotate(schedules_count=Count("schedules"))
