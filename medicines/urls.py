from django.urls import path

from . import views

app_name = "medicines"

urlpatterns = [
    path("", views.medicines, name="list"),
    path("<int:medicine_id>/", views.medicine_detail, name="detail"),
]
