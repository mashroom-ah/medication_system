"""Перенос данных из data/medication.sqlite в базу, управляемую Django ORM."""
import sqlite3
from datetime import date
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from homepage.models import User
from intakes.models import Intake
from medicines.models import Medicine
from schedules.models import Schedule


class Command(BaseCommand):
    help = "Импортирует данные из прежней SQLite-базы, сохраняя идентификаторы."

    def add_arguments(self, parser):
        default_source = Path(__file__).resolve().parents[3] / "data" / "medication.sqlite"
        parser.add_argument("--source", default=str(default_source))
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Очистить ORM-таблицы перед импортом",
        )

    def handle(self, *args, **options):
        source = Path(options["source"])
        if not source.is_file():
            raise CommandError(f"Не найдена исходная база: {source}")

        try:
            connection = sqlite3.connect(
                f"file:{source.resolve()}?mode=ro",
                uri=True,
            )
            connection.row_factory = sqlite3.Row
            users = connection.execute(
                "SELECT id, name, age FROM users ORDER BY id"
            ).fetchall()
            medicines = connection.execute(
                "SELECT id, name, dosage, unit FROM medicines ORDER BY id"
            ).fetchall()
            schedules = connection.execute(
                "SELECT id, user_id, medicine_id, hour, minute "
                "FROM schedules ORDER BY id"
            ).fetchall()
            intakes = connection.execute(
                "SELECT id, schedule_id, intake_date, taken "
                "FROM intakes ORDER BY id"
            ).fetchall()
            connection.close()
        except sqlite3.Error as exc:
            raise CommandError(
                f"Не удалось прочитать исходную базу: {exc}"
            ) from exc

        with transaction.atomic():
            if options["clear"]:
                Intake.objects.all().delete()
                Schedule.objects.all().delete()
                Medicine.objects.all().delete()
                User.objects.all().delete()

            for row in users:
                User.objects.update_or_create(
                    pk=row["id"],
                    defaults={"name": row["name"], "age": row["age"]},
                )
            for row in medicines:
                Medicine.objects.update_or_create(
                    pk=row["id"],
                    defaults={
                        "name": row["name"],
                        "dosage": row["dosage"],
                        "unit": row["unit"],
                    },
                )
            for row in schedules:
                Schedule.objects.update_or_create(
                    pk=row["id"],
                    defaults={
                        "user_id": row["user_id"],
                        "medicine_id": row["medicine_id"],
                        "hour": row["hour"],
                        "minute": row["minute"],
                    },
                )
            for row in intakes:
                try:
                    intake_date = date.fromisoformat(row["intake_date"])
                except ValueError as exc:
                    raise CommandError(
                        f"Некорректная дата в записи приёма {row['id']}"
                    ) from exc
                Intake.objects.update_or_create(
                    pk=row["id"],
                    defaults={
                        "schedule_id": row["schedule_id"],
                        "intake_date": intake_date,
                        "status": "taken" if bool(row["taken"]) else "missed",
                    },
                )

        summary = (
            f"Импорт завершён: пользователей={len(users)}, лекарств={len(medicines)}, "
            f"расписаний={len(schedules)}, приёмов={len(intakes)}."
        )
        self.stdout.write(self.style.SUCCESS(summary))
