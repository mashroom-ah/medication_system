from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [("schedules", "0001_initial")]
    operations = [
        migrations.CreateModel(
            name="Intake",
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
                ("intake_date", models.DateField(verbose_name="Дата приёма")),
                ("taken", models.BooleanField(default=True, verbose_name="Принято")),
                (
                    "schedule",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="intakes",
                        to="schedules.schedule",
                        verbose_name="Расписание",
                    ),
                ),
            ],
            options={
                "ordering": ["-intake_date", "-id"],
                "verbose_name": "Приём лекарства",
                "verbose_name_plural": "История приёмов",
                "indexes": [
                    models.Index(fields=["intake_date"], name="intake_date_idx"),
                    models.Index(
                        fields=["schedule", "intake_date"],
                        name="intake_sched_date_idx",
                    ),
                ],
            },
        ),
    ]
