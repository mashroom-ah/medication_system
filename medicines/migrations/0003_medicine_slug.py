from django.db import migrations, models
from django.utils.text import slugify
from unidecode import unidecode


def populate_slugs(apps, schema_editor):
    Medicine = apps.get_model("medicines", "Medicine")
    used = set()
    for medicine in Medicine.objects.order_by("pk").iterator():
        base = slugify(unidecode(medicine.name)) or "medicine"
        candidate = f"{base[:160]}-{medicine.pk}"
        suffix = 2
        while candidate in used:
            tail = f"-{suffix}"
            candidate = f"{base[:180-len(tail)]}-{medicine.pk}{tail}"
            suffix += 1
        medicine.slug = candidate
        medicine.save(update_fields=["slug"])
        used.add(candidate)


class Migration(migrations.Migration):
    dependencies = [("medicines", "0002_alter_medicine_dosage_alter_medicine_name_and_more")]

    operations = [
        migrations.AddField(
            model_name="medicine",
            name="slug",
            field=models.SlugField(
                blank=True, db_index=False, editable=False, max_length=180, null=True,
                verbose_name="Адрес (slug)",
            ),
        ),
        migrations.RunPython(populate_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="medicine",
            name="slug",
            field=models.SlugField(
                db_index=False, editable=False, max_length=180, unique=True,
                verbose_name="Адрес (slug)",
                help_text="Уникальная часть адреса подробной страницы лекарства.",
            ),
        ),
    ]
