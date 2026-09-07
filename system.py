from datetime import datetime


# Пользователь
user_name = 'Новикова Мария'
user_age = 19

# Препарат
medicine_name = 'Аскорбиновая кислота'
medicine_dosage = 10
medicine_unit = 'мг'

# Расписание
scheduled_hour = 12
scheduled_minute = 0

# Приём
is_taken = False

current_time = datetime.now()


def create_user(name: str, age: int):
    return name, age


def create_medicine(name: str, dosage: int, unit: str):
    return name, dosage, unit


def create_schedule(hour: int = 12, minute: int = 0):
    return hour, minute


def check_schedule():
    if is_taken:
        status = "Препарат уже принят"
    else:
        current_hour = current_time.hour
        current_minute = current_time.minute

        if (
            current_hour > scheduled_hour
            or (
                current_hour == scheduled_hour
                and current_minute >= scheduled_minute
            )
        ):
            status = "Необходимо принять препарат."
        else:
            minutes_left = (
                (scheduled_hour - current_hour) * 60
                + (scheduled_minute - current_minute)
            )

            status = (
                f"Время приема еще не наступило. "
                f"Осталось примерно {minutes_left} мин."
            )

    return status


# Приём препарата
def take_medicine():
    return True


print("=== Система учёта лекарств ===")
print()

# Тест функции create_user()
print("Создание пользователя")

input_name: str = input("Введите имя пользователя: ")
input_age: int = int(input("Введите возраст: "))

user_name, user_age = create_user(input_name, input_age)

print(f"Пользователь создан: {user_name}, {user_age} лет")
print()


# Тест функции create_medicine()
print("Создание препарата")

input_medicine_name: str = input("Введите название препарата: ")
input_dosage: int = int(input("Введите дозировку: "))
input_unit: str = input("Введите единицу измерения: ")

medicine_name, medicine_dosage, medicine_unit = create_medicine(
    input_medicine_name,
    input_dosage,
    input_unit
)

print(
    f"Препарат создан: {medicine_name}, "
    f"{medicine_dosage} {medicine_unit}"
)
print()


# Тест функции create_schedule()
print("Создание расписания")

scheduled_hour = int(input("Введите час приема: "))
scheduled_minute = int(input("Введите минуты приема: "))

scheduled_hour, scheduled_minute = create_schedule(
    scheduled_hour,
    scheduled_minute
)

print(
    f"Расписание создано: "
    f"{scheduled_hour:02d}:{scheduled_minute:02d}"
)
print()


# Тест функции check_schedule()
print("Проверка расписания")

print(f"Текущее время: {current_time.strftime('%H:%M')}")
print(f"Запланированное время: {scheduled_hour:02d}:{scheduled_minute:02d}")

print(f"Результат: {check_schedule()}")
print()


# Тест функции take_medicine()
print("Приём препарата")

answer: str = input("Принять препарат сейчас? (да/нет): ")

if answer.lower() == "да":
    is_taken = take_medicine()
    print("Препарат принят.")

    # Повторно проверяем расписание
    print(f"Результат повторной проверки: {check_schedule()}")
else:
    print("Приём препарата отменён.")