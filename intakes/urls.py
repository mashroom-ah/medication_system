from django.urls import path

from . import views

app_name = "intakes"

urlpatterns = [
    path("", views.intakes, name="list"),
    path("<int:intake_id>/", views.intake_detail, name="detail"),
]
