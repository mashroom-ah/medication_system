from django.db import migrations, models
import django.db.models.deletion
from django.db.models import Q


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ("homepage", "0001_initial"),
        ("medicines", "0001_initial"),
    ]
    operations = [
        migrations.CreateModel(
            name="Schedule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("hour", models.PositiveSmallIntegerField(verbose_name="Час")),
                ("minute", models.PositiveSmallIntegerField(verbose_name="Минута")),
                (
                    "medicine",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="schedules",
                        to="medicines.medicine",
                        verbose_name="Лекарство",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="schedules",
                        to="homepage.user",
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "ordering": ["hour", "minute", "id"],
                "verbose_name": "Расписание",
                "verbose_name_plural": "Расписания",
                "constraints": [
                    models.CheckConstraint(
                        condition=Q(hour__gte=0, hour__lte=23),
                        name="schedule_hour_0_23",
                    ),
                    models.CheckConstraint(
                        condition=Q(minute__gte=0, minute__lte=59),
                        name="schedule_minute_0_59",
                    ),
                ],
            },
        ),
    ]
