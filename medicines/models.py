from django.db import models
from django.db.models import Q


class Medicine(models.Model):
    """Лекарственный препарат."""

    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name="Название",
    )
    dosage = models.FloatField(verbose_name="Дозировка")
    unit = models.CharField(
        max_length=40,
        verbose_name="Единица измерения",
    )
    description = models.TextField(
        blank=True,
        default="",
        verbose_name="Описание",
    )

    class Meta:
        ordering = ["dosage", "name", "id"]
        verbose_name = "Лекарство"
        verbose_name_plural = "Лекарства"
        constraints = [
            models.CheckConstraint(
                condition=Q(dosage__gt=0),
                name="medicine_dosage_positive",
            ),
        ]

    def __str__(self):
        return f"{self.name} — {self.dosage:g} {self.unit}"