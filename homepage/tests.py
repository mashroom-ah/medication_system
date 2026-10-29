from django.test import TestCase
from django.urls import reverse
from homepage.models import User
from medicines.models import Medicine
from schedules.models import Schedule
from intakes.models import Intake
from datetime import date


class HomepageORMTests(TestCase):
    def test_homepage(self):
        self.assertEqual(self.client.get(reverse("homepage:index")).status_code, 200)

    def test_statistics_uses_orm(self):
        user = User.objects.create(name="Тест", age=20)
        medicine = Medicine.objects.create(name="Тест-препарат", dosage=5, unit="мг")
        schedule = Schedule.objects.create(user=user, medicine=medicine, hour=12, minute=0)
        Intake.objects.create(schedule=schedule, intake_date=date.today(), taken=True)
        response = self.client.get(reverse("homepage:statistics"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Тест-препарат")
        self.assertContains(response, "Дополнительные показатели")
