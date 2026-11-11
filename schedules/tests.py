from datetime import date
from django.test import TestCase
from django.urls import reverse
from homepage.models import User
from medicines.models import Medicine
from .models import Schedule
from intakes.models import Intake


class ScheduleORMTests(TestCase):
    def setUp(self):
        user = User.objects.create(name="Иван", age=42)
        medicine = Medicine.objects.create(name="Препарат", dosage=10, unit="мг")
        self.schedule = Schedule.objects.create(
            user=user, medicine=medicine, hour=8, minute=0
        )

    def test_list_and_related_models(self):
        response = self.client.get(reverse("schedules:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Препарат")
        self.assertEqual(self.schedule.user.name, "Иван")
        self.schedule.refresh_from_db()
        self.assertEqual(self.schedule.total_minutes, 480)
        self.assertFalse(self.schedule.is_night)

    def test_generated_total_minutes(self):
        self.assertEqual(self.schedule.total_minutes, 480)
        self.schedule.hour = 9
        self.schedule.save(update_fields=["hour"])
        self.schedule.refresh_from_db()
        self.assertEqual(self.schedule.total_minutes, 540)
        self.schedule.hour = 23
        self.schedule.save(update_fields=["hour"])
        self.schedule.refresh_from_db()
        self.assertTrue(self.schedule.is_night)

    def test_detail_missing_returns_404(self):
        response = self.client.get(reverse("schedules:detail", args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_intake_exists_query(self):
        Intake.objects.create(
            schedule=self.schedule, intake_date=date.today(),
            status=Intake.Status.TAKEN,
        )
        self.assertTrue(self.schedule.intakes.filter(
            intake_date=date.today(), status=Intake.Status.TAKEN
        ).exists())
