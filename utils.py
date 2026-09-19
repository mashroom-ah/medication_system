def input_int(prompt: str) -> int:
    """Запрашивает целое число с повтором при ошибке."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: необходимо ввести целое число.")


def input_positive_int(prompt: str) -> int:
    """Запрашивает положительное целое число."""
    while True:
        value = input_int(prompt)
        if value > 0:
            return value
        print("Ошибка: число должно быть больше нуля.")


def input_age(prompt: str) -> int:
    """Запрашивает возраст от 1 до 120 лет."""
    while True:
        age = input_int(prompt)
        if 0 < age <= 120:
            return age
        print("Ошибка: возраст должен быть от 1 до 120.")


def input_time(prompt: str) -> tuple[int, int]:
    """Запрашивает время в формате ЧЧ:ММ."""
    while True:
        try:
            value = input(prompt)
            hour, minute = map(int, value.split(":"))
            if not 0 <= hour <= 23:
                raise ValueError
            if not 0 <= minute <= 59:
                raise ValueError
            return hour, minute
        except ValueError:
            print(
                "Ошибка. Введите время в формате ЧЧ:ММ, "
                "например 12:30."
            )


def input_date(prompt: str) -> str:
    """Запрашивает дату в формате ГГГГ-ММ-ДД."""
    while True:
        value = input(prompt)
        parts = value.split("-")
        if len(parts) == 3 and all(part.isdigit() for part in parts):
            year, month, day = map(int, parts)
            if 1 <= month <= 12 and 1 <= day <= 31:
                return value
        print(
            "Ошибка. Введите дату в формате ГГГГ-ММ-ДД, "
            "например 2026-09-20."
        )
