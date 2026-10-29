from django.contrib import admin
from .models import Medicine


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "dosage", "unit")
    search_fields = ("name", "unit")
    list_filter = ("unit",)
