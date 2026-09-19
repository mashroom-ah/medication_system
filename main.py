from __future__ import annotations

from datetime import date, datetime

from models import Intake, Medicine, Schedule, User
from models.intakes import (
    cancel_intake,
    create_intake,
    is_medicine_taken,
    show_intakes,
)
from models.medicines import (
    add_medicine,
    filter_medicines_by_dosage,
    find_medicine,
    show_medicines,
)
from models.schedules import add_schedule, show_schedules
from models.users import add_user, find_user, show_users
from storage import (
    load_intakes,
    load_medicines,
    load_schedules,
    load_users,
    save_intakes,
    save_medicines,
    save_schedules,
    save_users,
)
from utils import input_age, input_date, input_positive_int, input_time

USERS_FILE = "data/users.json"
MEDICINES_FILE = "data/medicines.json"
SCHEDULES_FILE = "data/schedules.json"
INTAKES_FILE = "data/intakes.json"


def find_by_id(items: list, item_id: int) -> object | None:
    """Находит объект с указанным идентификатором."""
    for item in items:
        if item.id == item_id:
            return item
    return None


def create_new_schedule(
    schedules: list[Schedule],
    users: list[User],
    medicines: list[Medicine],
) -> None:
    """Создаёт расписание после проверки связанных объектов."""
    user_id = input_positive_int("ID пользователя: ")
    medicine_id = input_positive_int("ID лекарства: ")
    hour, minute = input_time("Введите время приема (ЧЧ:ММ): ")

    user = find_by_id(users, user_id)
    medicine = find_by_id(medicines, medicine_id)

    if not isinstance(user, User):
        print("Пользователь не найден.")
        return
    if not isinstance(medicine, Medicine):
        print("Лекарство не найдено.")
        return

    schedule = add_schedule(
        schedules,
        user,
        medicine,
        hour,
        minute,
    )
    save_schedules(SCHEDULES_FILE, schedules)
    print(f"Расписание добавлено. ID: {schedule.id}")


def check_schedule(
    schedules: list[Schedule],
    intakes: list[Intake],
) -> None:
    """Показывает статус выбранного расписания."""
    schedule_id = input_positive_int("ID расписания: ")
    schedule = find_by_id(schedules, schedule_id)
    if not isinstance(schedule, Schedule):
        print("Расписание не найдено.")
        return

    today = date.today().isoformat()
    taken = is_medicine_taken(intakes, schedule.id, today)
    print(schedule.get_status(taken, datetime.now()))


def take_medicine(
    schedules: list[Schedule],
    intakes: list[Intake],
) -> None:
    """Записывает приём лекарства за текущую дату."""
    schedule_id = input_positive_int("ID расписания: ")
    schedule = find_by_id(schedules, schedule_id)
    if not isinstance(schedule, Schedule):
        print("Расписание не найдено.")
        return

    today = date.today().isoformat()
    if is_medicine_taken(intakes, schedule.id, today):
        print("Прием на сегодня уже записан.")
        return

    intake = create_intake(intakes, schedule)
    save_intakes(INTAKES_FILE, intakes)
    print(f"Прием записан: {intake.date}")


def cancel_medicine_intake(intakes: list[Intake]) -> None:
    """Отменяет запись о приёме за выбранную дату."""
    schedule_id = input_positive_int("ID расписания: ")
    intake_date = input_date("Введите дату (ГГГГ-ММ-ДД): ")
    result = cancel_intake(intakes, schedule_id, intake_date)
    if result:
        save_intakes(INTAKES_FILE, intakes)
        print("Запись о приеме отменена.")
    else:
        print("Запись о приеме не найдена.")


def main() -> None:
    """Запускает основное меню программы."""
    users = load_users(USERS_FILE)
    medicines = load_medicines(MEDICINES_FILE)
    schedules = load_schedules(SCHEDULES_FILE, users, medicines)
    intakes = load_intakes(INTAKES_FILE, schedules)

    while True:
        print("\n=== Система учета лекарств ===")
        print("1. Добавить пользователя")
        print("2. Показать пользователей")
        print("3. Найти пользователя")
        print("4. Добавить лекарство")
        print("5. Показать лекарства")
        print("6. Найти лекарство")
        print("7. Фильтр лекарств по дозировке")
        print("8. Добавить расписание")
        print("9. Показать расписания")
        print("10. Проверить время приема")
        print("11. Принять лекарство")
        print("12. Отменить прием")
        print("13. Показать приемы за дату")
        print("0. Выход")

        choice = input("Выберите пункт: ")

        try:
            if choice == "1":
                name = input("Введите имя: ")
                age = input_age("Введите возраст: ")
                user = add_user(users, name, age)
                save_users(USERS_FILE, users)
                print(f"Пользователь добавлен. ID: {user.id}")

            elif choice == "2":
                show_users(users)

            elif choice == "3":
                query = input("Введите имя для поиска: ")
                results = find_user(users, query)
                if results:
                    show_users(results)
                else:
                    print("Пользователь не найден.")

            elif choice == "4":
                name = input("Введите название лекарства: ")
                dosage = input_positive_int("Введите дозировку: ")
                unit = input("Введите единицу измерения: ")
                medicine = add_medicine(
                    medicines,
                    name,
                    dosage,
                    unit,
                )
                save_medicines(MEDICINES_FILE, medicines)
                print(f"Лекарство добавлено. ID: {medicine.id}")

            elif choice == "5":
                show_medicines(medicines)

            elif choice == "6":
                query = input(
                    "Введите название лекарства для поиска: "
                )
                results = find_medicine(medicines, query)
                if results:
                    show_medicines(results)
                else:
                    print("Лекарство не найдено.")

            elif choice == "7":
                min_dosage = input_positive_int(
                    "Минимальная дозировка: "
                )
                results = filter_medicines_by_dosage(
                    medicines,
                    min_dosage,
                )
                if results:
                    show_medicines(results)
                else:
                    print("Лекарств с такой дозировкой нет.")

            elif choice == "8":
                create_new_schedule(schedules, users, medicines)

            elif choice == "9":
                show_schedules(schedules)

            elif choice == "10":
                check_schedule(schedules, intakes)

            elif choice == "11":
                take_medicine(schedules, intakes)

            elif choice == "12":
                cancel_medicine_intake(intakes)

            elif choice == "13":
                intake_date = input_date(
                    "Введите дату (ГГГГ-ММ-ДД): "
                )
                show_intakes(intakes, intake_date)

            elif choice == "0":
                save_users(USERS_FILE, users)
                save_medicines(MEDICINES_FILE, medicines)
                save_schedules(SCHEDULES_FILE, schedules)
                save_intakes(INTAKES_FILE, intakes)
                print("Программа завершена.")
                break

            else:
                print("Ошибка: такого пункта меню нет.")

        except (OSError, ValueError, KeyError) as error:
            print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()
