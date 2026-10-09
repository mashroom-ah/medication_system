from django.urls import path

from . import views

urlpatterns = [
    path("", views.intakes, name="intakes"),
    path("<int:intake_id>/", views.intake_detail, name="intake_detail"),
]
