from django.db import migrations, models
from django.db.models import Case, F, Q, Value, When


class Migration(migrations.Migration):
    dependencies = [("schedules", "0002_alter_schedule_hour_alter_schedule_medicine_and_more")]

    operations = [
        migrations.AddField(
            model_name="schedule",
            name="is_night",
            field=models.GeneratedField(
                db_persist=True,
                expression=Case(
                    When(Q(hour__gte=22) | Q(hour__lt=6), then=Value(True)),
                    default=Value(False),
                    output_field=models.BooleanField(),
                ),
                output_field=models.BooleanField(),
                help_text="Вычисляется БД: с 22:00 до 05:59.",
                verbose_name="Ночное расписание",
            ),
        ),
        migrations.AddField(
            model_name="schedule",
            name="total_minutes",
            field=models.GeneratedField(
                db_persist=True,
                expression=F("hour") * 60 + F("minute"),
                output_field=models.PositiveSmallIntegerField(),
                help_text="Вычисляется базой данных из часа и минуты.",
                verbose_name="Минут от начала суток",
            ),
        ),
    ]
