from django.db import models


class Intake(models.Model):
    """Фактическая запись о приёме по расписанию."""

    schedule = models.ForeignKey(
        "schedules.Schedule",
        on_delete=models.PROTECT,
        related_name="intakes",
        verbose_name="Расписание",
        help_text="Расписание, по которому учитывается приём.",
    )
    intake_date = models.DateField(
        verbose_name="Дата приёма",
        help_text="Дата фактического приёма лекарства.",
    )
    taken = models.BooleanField(
        default=True,
        verbose_name="Принято",
        help_text="Отмечает, было ли лекарство принято.",
    )

    class Meta:
        ordering = ["-intake_date", "-id"]
        verbose_name = "Приём лекарства"
        verbose_name_plural = "История приёмов"
        indexes = [
            models.Index(fields=["intake_date"], name="intake_date_idx"),
            models.Index(
                fields=["schedule", "intake_date"],
                name="intake_sched_date_idx",
            ),
        ]

    @property
    def date(self):
        """Совместимость с существующими шаблонами веб-интерфейса."""
        return self.intake_date

    def __str__(self):
        return f"{self.schedule.medicine.name}: {self.intake_date}"