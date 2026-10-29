from datetime import date

from django.test import TestCase
from django.urls import reverse

from homepage.models import User
from medicines.models import Medicine
from schedules.models import Schedule
from .models import Intake


class IntakeORMTests(TestCase):
    def setUp(self):
        user = User.objects.create(name="Мария", age=25)
        medicine = Medicine.objects.create(name="Витамин", dosage=20, unit="мг")
        schedule = Schedule.objects.create(
            user=user,
            medicine=medicine,
            hour=9,
            minute=15,
        )
        self.intake = Intake.objects.create(
            schedule=schedule,
            intake_date=date(2026, 10, 1),
            taken=False,
        )

    def test_date_and_status_filters(self):
        response = self.client.get(
            reverse("intakes:list"),
            {"date": "2026-10-01", "status": "missed"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Витамин")

    def test_invalid_date_does_not_crash(self):
        response = self.client.get(
            reverse("intakes:list"), {"date": "not-a-date"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Некорректная дата")

    def test_detail_and_404(self):
        detail_url = reverse("intakes:detail", args=[self.intake.pk])
        missing_url = reverse("intakes:detail", args=[999])
        self.assertEqual(self.client.get(detail_url).status_code, 200)
        self.assertEqual(self.client.get(missing_url).status_code, 404)
