def input_int(prompt: str) -> int:
    """Запрашивает целое число."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: необходимо ввести целое число.")


def input_positive_int(prompt: str) -> int:
    """Запрашивает целое положительное число."""
    while True:
        value = input_int(prompt)

        if value > 0:
            return value

        print("Ошибка: число должно быть больше нуля.")


def input_age(prompt: str) -> int:
    """Запрашивает возраст."""
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
                "Ошибка. Введите время в формате "
                "ЧЧ:ММ, например 12:30."
            )
