from datetime import date

from django.test import TestCase
from django.urls import reverse

from homepage.models import User
from intakes.models import Intake
from schedules.models import Schedule
from .models import Medicine


class MedicineORMTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(name="Анна", age=30)
        cls.medicine = Medicine.objects.create(
            name="Аспирин", dosage=100, unit="мг"
        )
        cls.schedule = Schedule.objects.create(
            user=cls.user,
            medicine=cls.medicine,
            hour=8,
            minute=30,
        )
        Intake.objects.create(
            schedule=cls.schedule,
            intake_date=date(2026, 10, 1),
            status=Intake.Status.TAKEN,
        )
        Medicine.objects.create(name="Витамин C", dosage=500, unit="мг")

    def test_list_search_and_filter(self):
        response = self.client.get(
            reverse("medicines:list"),
            {"q": "аспир", "min_dosage": "50"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Аспирин")
        self.assertNotContains(response, "Витамин C")

    def test_invalid_dosage_is_ignored(self):
        response = self.client.get(
            reverse("medicines:list"), {"min_dosage": "abc"}
        )
        self.assertEqual(response.status_code, 200)

    def test_detail_404(self):
        response = self.client.get(
            reverse("medicines:detail", kwargs={"slug": "missing-medicine"})
        )
        self.assertEqual(response.status_code, 404)

    def test_slug_detail_and_absolute_url(self):
        response = self.client.get(self.medicine.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Аспирин")

    def test_crud_and_relationships(self):
        obj = Medicine.objects.create(name="Тест", dosage=1, unit="мг")
        obj.dosage = 2
        obj.save()
        self.assertEqual(Medicine.objects.get(pk=obj.pk).dosage, 2)
        self.assertEqual(self.schedule.medicine.name, "Аспирин")
        self.assertEqual(self.user.schedules.count(), 1)
        self.assertTrue(self.medicine.slug.startswith("aspirin-"))
        self.assertEqual(
            self.medicine.get_absolute_url(),
            reverse("medicines:detail", kwargs={"slug": self.medicine.slug}),
        )
        obj.delete()
        self.assertFalse(Medicine.objects.filter(name="Тест").exists())

    def test_sorting_and_pagination(self):
        for number in range(12):
            Medicine.objects.create(
                name=f"Препарат {number}", dosage=number + 1, unit="мг"
            )
        response = self.client.get(
            reverse("medicines:list"), {"sort": "-name", "page": 2}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page_obj"].number, 2)
        self.assertEqual(len(response.context["medicines"]), 4)
