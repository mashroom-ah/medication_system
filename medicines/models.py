from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode


class Medicine(models.Model):
    """Лекарственный препарат."""

    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name="Название",
        blank=True,
        help_text="Название лекарственного препарата.",
    )
    slug = models.SlugField(
        max_length=180,
        unique=True,
        db_index=False,
        editable=False,
        verbose_name="Адрес (slug)",
        help_text="Уникальная часть адреса подробной страницы лекарства.",
    )
    dosage = models.FloatField(
        verbose_name="Дозировка",
        help_text="Количество действующего вещества.",
    )
    unit = models.CharField(
        max_length=40,
        verbose_name="Единица измерения",
        help_text="Например, мг или мл.",
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

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(unidecode(self.name)) or "medicine"
            if self.pk is None:
                kwargs.pop("update_fields", None)
                super().save(*args, **kwargs)
                self.slug = f"{base[:160]}-{self.pk}"
                super().save(update_fields=["slug"])
                return
            self.slug = f"{base[:160]}-{self.pk}"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("medicines:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.name} — {self.dosage:g} {self.unit}"
