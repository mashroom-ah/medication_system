from django.db import migrations, models
from django.db.models import Q


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Medicine",
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
                (
                    "name",
                    models.CharField(
                        db_index=True,
                        max_length=200,
                        verbose_name="Название",
                    ),
                ),
                ("dosage", models.FloatField(verbose_name="Дозировка")),
                (
                    "unit",
                    models.CharField(max_length=40, verbose_name="Единица измерения"),
                ),
            ],
            options={
                "ordering": ["dosage", "name", "id"],
                "verbose_name": "Лекарство",
                "verbose_name_plural": "Лекарства",
                "constraints": [
                    models.CheckConstraint(
                        condition=Q(dosage__gt=0),
                        name="medicine_dosage_positive",
                    ),
                ],
            },
        ),
    ]
