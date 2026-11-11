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
            status=Intake.Status.MISSED,
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

    def test_queryset_manager_methods(self):
        self.assertEqual(Intake.objects.missed().count(), 1)
        self.assertEqual(Intake.objects.for_date(date(2026, 10, 1)).count(), 1)
        self.intake.status = Intake.Status.SKIPPED
        self.intake.save(update_fields=["status"])
        self.assertEqual(Intake.objects.skipped().count(), 1)
        self.intake.status = Intake.Status.TAKEN
        self.intake.save(update_fields=["status"])
        self.assertTrue(self.intake.taken)
        self.assertEqual(Intake.objects.taken().count(), 1)

    def test_detail_and_404(self):
        detail_url = reverse("intakes:detail", args=[self.intake.pk])
        missing_url = reverse("intakes:detail", args=[999])
        self.assertEqual(self.client.get(detail_url).status_code, 200)
        self.assertEqual(self.client.get(missing_url).status_code, 404)

    def test_select_related_avoids_n_plus_one(self):
        with self.assertNumQueries(1):
            rows = list(Intake.objects.select_related(
                "schedule__user", "schedule__medicine"
            ))
            for row in rows:
                _ = row.schedule.user.name
                _ = row.schedule.medicine.name

    def test_related_user_medicine_filters_and_sorting(self):
        response = self.client.get(reverse("intakes:list"), {
            "user": str(self.intake.schedule.user_id),
            "medicine": str(self.intake.schedule.medicine_id),
            "sort": "medicine",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page_obj"].paginator.count, 1)

    def test_pagination(self):
        for day in range(2, 14):
            Intake.objects.create(
                schedule=self.intake.schedule,
                intake_date=date(2026, 10, day),
                status=Intake.Status.MISSED,
            )
        response = self.client.get(reverse("intakes:list"), {"page": 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page_obj"].number, 2)
        self.assertEqual(len(response.context["intakes"]), 3)
