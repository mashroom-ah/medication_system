from django.db import models
from django.db.models import Q


class Schedule(models.Model):
    """Расписание приёма конкретного лекарства пользователем."""

    user = models.ForeignKey(
        "homepage.User",
        on_delete=models.PROTECT,
        related_name="schedules",
        verbose_name="Пользователь",
        help_text="Пользователь, для которого создано расписание.",
    )
    medicine = models.ForeignKey(
        "medicines.Medicine",
        on_delete=models.PROTECT,
        related_name="schedules",
        verbose_name="Лекарство",
        help_text="Лекарство, которое нужно принимать.",
    )
    hour = models.PositiveSmallIntegerField(
        verbose_name="Час",
        help_text="Час приёма от 0 до 23.",
    )
    minute = models.PositiveSmallIntegerField(
        verbose_name="Минута",
        help_text="Минута приёма от 0 до 59.",
    )

    class Meta:
        ordering = ["hour", "minute", "id"]
        verbose_name = "Расписание"
        verbose_name_plural = "Расписания"
        constraints = [
            models.CheckConstraint(
                condition=Q(hour__gte=0) & Q(hour__lte=23),
                name="schedule_hour_0_23",
            ),
            models.CheckConstraint(
                condition=Q(minute__gte=0) & Q(minute__lte=59),
                name="schedule_minute_0_59",
            ),
        ]

    def __str__(self):
        return (
            f"{self.medicine.name} для {self.user.name}, "
            f"{self.hour:02d}:{self.minute:02d}"
        )