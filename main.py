from datetime import date, datetime

from intakes import (
    cancel_intake,
    create_intake,
    get_intakes_by_date,
    is_medicine_taken,
)
from medicines import (
    add_medicine,
    filter_medicines_by_dosage,
    find_medicine,
    sort_medicines,
)
from schedules import (
    add_schedule,
    get_schedule_status,
    sort_schedules,
)
from storage import load_data, save_data
from users import add_user, find_user, sort_users
from utils import (
    input_age,
    input_positive_int,
    input_time,
)


USERS_FILE = "data/users.json"
MEDICINES_FILE = "data/medicines.json"
SCHEDULES_FILE = "data/schedules.json"
INTAKES_FILE = "data/intakes.json"


def show_users(users: list[dict]) -> None:
    """Выводит список пользователей."""
    if not users:
        print("Пользователей нет.")
        return

    for user in sort_users(users):
        print(
            f'ID: {user["id"]}, '
            f'Имя: {user["name"]}, '
            f'Возраст: {user["age"]}'
        )


def show_medicines(medicines: list[dict]) -> None:
    """Выводит список лекарств."""
    if not medicines:
        print("Лекарств нет.")
        return

    for medicine in sort_medicines(medicines):
        print(
            f'ID: {medicine["id"]}, '
            f'Название: {medicine["name"]}, '
            f'Дозировка: {medicine["dosage"]} '
            f'{medicine["unit"]}'
        )


def show_schedules(
    schedules: list[dict],
    medicines: list[dict]
) -> None:
    """Выводит список расписаний."""
    if not schedules:
        print("Расписаний нет.")
        return

    for schedule in sort_schedules(schedules):
        medicine = None

        for item in medicines:
            if item["id"] == schedule["medicine_id"]:
                medicine = item
                break

        if medicine is not None:
            medicine_name = medicine["name"]
        else:
            medicine_name = "Неизвестное лекарство"

        print(
            f'ID: {schedule["id"]}, '
            f'Лекарство: {medicine_name}, '
            f'Время: {schedule["hour"]:02d}:'
            f'{schedule["minute"]:02d}'
        )


def show_intakes(
    intakes: list[dict],
    intake_date: str
) -> None:
    """Выводит приемы за указанную дату."""
    daily_intakes = get_intakes_by_date(
        intakes,
        intake_date
    )

    if not daily_intakes:
        print("За эту дату приемов нет.")
        return

    for intake in daily_intakes:
        if intake["taken"]:
            status = "принят"
        else:
            status = "не принят"

        print(
            f'ID: {intake["id"]}, '
            f'Расписание: {intake["schedule_id"]}, '
            f'Дата: {intake["date"]}, '
            f'Статус: {status}'
        )


def main() -> None:
    """Запускает основное меню программы."""
    users = load_data(USERS_FILE)
    medicines = load_data(MEDICINES_FILE)
    schedules = load_data(SCHEDULES_FILE)
    intakes = load_data(INTAKES_FILE)

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

                user = add_user(
                    users,
                    name,
                    age
                )

                save_data(
                    USERS_FILE,
                    users
                )

                print(
                    f'Пользователь добавлен. '
                    f'ID: {user["id"]}'
                )

            elif choice == "2":
                show_users(users)

            elif choice == "3":
                query = input(
                    "Введите имя для поиска: "
                )

                results = find_user(
                    users,
                    query
                )

                if results:
                    show_users(results)
                else:
                    print("Пользователь не найден.")

            elif choice == "4":
                name = input(
                    "Введите название лекарства: "
                )

                dosage = input_positive_int(
                    "Введите дозировку: "
                )

                unit = input(
                    "Введите единицу измерения: "
                )

                medicine = add_medicine(
                    medicines,
                    name,
                    dosage,
                    unit
                )

                save_data(
                    MEDICINES_FILE,
                    medicines
                )

                print(
                    f'Лекарство добавлено. '
                    f'ID: {medicine["id"]}'
                )

            elif choice == "5":
                show_medicines(medicines)

            elif choice == "6":
                query = input(
                    "Введите название лекарства "
                    "для поиска: "
                )

                results = find_medicine(
                    medicines,
                    query
                )

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
                    min_dosage
                )

                if results:
                    show_medicines(results)
                else:
                    print(
                        "Лекарств с такой дозировкой нет."
                    )

            elif choice == "8":
                user_id = input_positive_int(
                    "ID пользователя: "
                )

                medicine_id = input_positive_int(
                    "ID лекарства: "
                )

                hour, minute = input_time(
                    "Введите время приема (ЧЧ:ММ): "
                )

                user_exists = False

                for user in users:
                    if user["id"] == user_id:
                        user_exists = True
                        break

                medicine_exists = False

                for medicine in medicines:
                    if medicine["id"] == medicine_id:
                        medicine_exists = True
                        break

                if not user_exists:
                    print("Пользователь не найден.")
                    continue

                if not medicine_exists:
                    print("Лекарство не найдено.")
                    continue

                schedule = add_schedule(
                    schedules,
                    user_id,
                    medicine_id,
                    hour,
                    minute
                )

                save_data(
                    SCHEDULES_FILE,
                    schedules
                )

                print(
                    f'Расписание добавлено. '
                    f'ID: {schedule["id"]}'
                )

            elif choice == "9":
                show_schedules(
                    schedules,
                    medicines
                )

            elif choice == "10":
                schedule_id = input_positive_int(
                    "ID расписания: "
                )

                schedule = None

                for item in schedules:
                    if item["id"] == schedule_id:
                        schedule = item
                        break

                if schedule is None:
                    print("Расписание не найдено.")
                    continue

                today = date.today().isoformat()

                taken = is_medicine_taken(
                    intakes,
                    schedule_id,
                    today
                )

                status = get_schedule_status(
                    schedule,
                    taken,
                    datetime.now()
                )

                print(status)

            elif choice == "11":
                schedule_id = input_positive_int(
                    "ID расписания: "
                )

                schedule = None

                for item in schedules:
                    if item["id"] == schedule_id:
                        schedule = item
                        break

                if schedule is None:
                    print("Расписание не найдено.")
                    continue

                today = date.today().isoformat()

                already_taken = is_medicine_taken(
                    intakes,
                    schedule_id,
                    today
                )

                if already_taken:
                    print(
                        "Прием на сегодня уже записан."
                    )
                    continue

                intake = create_intake(
                    intakes,
                    schedule_id
                )

                save_data(
                    INTAKES_FILE,
                    intakes
                )

                print(
                    f'Прием записан: '
                    f'{intake["date"]}'
                )

            elif choice == "12":
                schedule_id = input_positive_int(
                    "ID расписания: "
                )

                intake_date = input(
                    "Введите дату (ГГГГ-ММ-ДД): "
                )

                result = cancel_intake(
                    intakes,
                    schedule_id,
                    intake_date
                )

                if result:
                    save_data(
                        INTAKES_FILE,
                        intakes
                    )

                    print(
                        "Запись о приеме отменена."
                    )
                else:
                    print(
                        "Запись о приеме не найдена."
                    )

            elif choice == "13":
                intake_date = input(
                    "Введите дату (ГГГГ-ММ-ДД): "
                )

                show_intakes(
                    intakes,
                    intake_date
                )

            elif choice == "0":
                print("Программа завершена.")
                break

            else:
                print(
                    "Ошибка: такого пункта меню нет."
                )

        except (OSError, ValueError) as error:
            print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()
