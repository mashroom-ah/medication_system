from django.db import models


class User(models.Model):
    """Пользователь приложения учёта лекарств."""

    name = models.CharField(max_length=150, verbose_name="Имя")
    age = models.PositiveSmallIntegerField(verbose_name="Возраст")

    class Meta:
        ordering = ["name", "id"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(age__gte=1) & models.Q(age__lte=120),
                name="user_age_1_120",
            ),
        ]

    def __str__(self):
        return self.name
