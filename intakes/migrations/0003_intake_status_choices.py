from django.db import migrations, models


def forwards(apps, schema_editor):
    Intake = apps.get_model("intakes", "Intake")
    for item in Intake.objects.all().iterator():
        item.status = "taken" if item.taken else "missed"
        item.save(update_fields=["status"])


def backwards(apps, schema_editor):
    Intake = apps.get_model("intakes", "Intake")
    for item in Intake.objects.all().iterator():
        item.taken = item.status == "taken"
        item.save(update_fields=["taken"])


class Migration(migrations.Migration):
    dependencies = [("intakes", "0002_alter_intake_intake_date_alter_intake_schedule_and_more")]

    operations = [
        migrations.AddField(
            model_name="intake",
            name="status",
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.RunPython(forwards, backwards),
        migrations.AlterField(
            model_name="intake",
            name="status",
            field=models.CharField(
                choices=[
                    ("taken", "Принято"),
                    ("missed", "Пропущено"),
                    ("skipped", "Пропущено по решению пользователя"),
                ],
                db_index=True,
                default="taken",
                help_text="Фактический результат приёма лекарства.",
                max_length=10,
                verbose_name="Статус приёма",
            ),
        ),
        migrations.RemoveField(model_name="intake", name="taken"),
        migrations.AddIndex(
            model_name="intake",
            index=models.Index(
                fields=["status", "intake_date"],
                name="intake_status_date_idx",
            ),
        ),
    ]
