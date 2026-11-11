from django.urls import path

from . import views

app_name = "medicines"

urlpatterns = [
    path("", views.medicines, name="list"),
    path("<str:slug>/", views.medicine_detail, name="detail"),
]
