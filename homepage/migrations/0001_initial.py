from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="User",
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
                ("name", models.CharField(max_length=150, verbose_name="Имя")),
                ("age", models.PositiveSmallIntegerField(verbose_name="Возраст")),
            ],
            options={
                "ordering": ["name", "id"],
                "verbose_name": "Пользователь",
                "verbose_name_plural": "Пользователи",
                "constraints": [
                    models.CheckConstraint(
                        condition=models.Q(("age__gte", 1), ("age__lte", 120)),
                        name="user_age_1_120",
                    ),
                ],
            },
        ),
    ]
