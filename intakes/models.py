from django.db import models


class IntakeQuerySet(models.QuerySet):
    """Повторно используемые выборки истории приёмов."""

    def taken(self):
        return self.filter(status=Intake.Status.TAKEN)

    def missed(self):
        return self.filter(status=Intake.Status.MISSED)

    def skipped(self):
        return self.filter(status=Intake.Status.SKIPPED)

    def for_date(self, value):
        return self.filter(intake_date=value)


class Intake(models.Model):
    """Фактическая запись о приёме по расписанию."""

    class Status(models.TextChoices):
        TAKEN = "taken", "Принято"
        MISSED = "missed", "Пропущено"
        SKIPPED = "skipped", "Пропущено по решению пользователя"

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
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.TAKEN,
        db_index=True,
        verbose_name="Статус приёма",
        help_text="Фактический результат приёма лекарства.",
    )

    objects = IntakeQuerySet.as_manager()

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
            models.Index(fields=["status", "intake_date"], name="intake_status_date_idx"),
        ]

    @property
    def taken(self):
        """Совместимость со старым шаблонным API: True только для принятого лекарства."""
        return self.status == self.Status.TAKEN

    @property
    def date(self):
        """Совместимость с существующими шаблонами веб-интерфейса."""
        return self.intake_date

    def __str__(self):
        return f"{self.schedule.medicine.name}: {self.intake_date} ({self.get_status_display()})"
