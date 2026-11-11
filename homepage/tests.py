from datetime import date

from django.test import TestCase
from django.urls import reverse

from homepage.models import User
from intakes.models import Intake
from medicines.models import Medicine
from schedules.models import Schedule


class HomepageORMTests(TestCase):
    def test_homepage(self):
        response = self.client.get(reverse("homepage:index"))
        self.assertEqual(response.status_code, 200)

    def test_context_processor_is_registered(self):
        response = self.client.get(reverse("homepage:index"))
        self.assertEqual(response.context["app_title"], "Мой приём")
        self.assertEqual(response.context["medicines_count"], 0)
        medicines_response = self.client.get(reverse("medicines:list"))
        self.assertEqual(medicines_response.context["app_title"], "Мой приём")

    def test_statistics_uses_orm(self):
        user = User.objects.create(name="Тест", age=20)
        medicine = Medicine.objects.create(
            name="Тест-препарат", dosage=5, unit="мг"
        )
        schedule = Schedule.objects.create(
            user=user, medicine=medicine, hour=12, minute=0
        )
        Intake.objects.create(
            schedule=schedule, intake_date=date.today(),
            status=Intake.Status.TAKEN,
        )
        response = self.client.get(reverse("homepage:statistics"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Тест-препарат")
        self.assertContains(response, "Дополнительные показатели")

    def test_admin_models_registered(self):
        from django.contrib import admin
        from homepage.models import User
        from medicines.models import Medicine
        from schedules.models import Schedule
        from intakes.models import Intake

        for model in (User, Medicine, Schedule, Intake):
            self.assertIn(model, admin.site._registry)
        self.assertTrue(admin.site._registry[User].inlines)
        self.assertTrue(admin.site._registry[Medicine].inlines)
        self.assertTrue(admin.site._registry[Schedule].inlines)
        self.assertIn("search_fields", admin.site._registry[Medicine].__class__.__dict__)
