import json


def load_data(filename: str) -> list[dict]:
    """Загружает список данных из файла JSON."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

            if not isinstance(data, list):
                raise ValueError("JSON должен содержать список.")

            return data

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        return []


def save_data(
        filename: str,
        data: list[dict]
) -> None:
    """Сохраняет список данных в файл JSON."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )

    except OSError as error:
        raise OSError(
            f"Не удалось сохранить файл {filename}: {error}"
        ) from error
