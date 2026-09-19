from __future__ import annotations


class Medicine:
    """Лекарственный препарат."""

    def __init__(
        self,
        medicine_id: int,
        name: str,
        dosage: int,
        unit: str,
    ) -> None:
        """Создаёт объект лекарства."""
        self.id = medicine_id
        self.name = name
        self.dosage = dosage
        self.unit = unit

    def __str__(self) -> str:
        """Возвращает строковое представление лекарства."""
        return (
            f"{self.name}, дозировка: {self.dosage} {self.unit}, "
            f"ID: {self.id}"
        )

    @staticmethod
    def validate_dosage(dosage: int) -> bool:
        """Проверяет корректность дозировки."""
        return dosage > 0

    @classmethod
    def from_data(cls, data: dict) -> Medicine:
        """Создаёт лекарство из данных JSON."""
        return cls(
            medicine_id=int(data["id"]),
            name=str(data["name"]),
            dosage=int(data["dosage"]),
            unit=str(data["unit"]),
        )

    def to_data(self) -> dict:
        """Преобразует лекарство в структуру для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "dosage": self.dosage,
            "unit": self.unit,
        }


def add_medicine(
    medicines: list[Medicine],
    name: str,
    dosage: int,
    unit: str,
) -> Medicine:
    """Создаёт лекарство и добавляет его в коллекцию."""
    if not Medicine.validate_dosage(dosage):
        raise ValueError("Дозировка должна быть больше нуля.")
    medicine_id = max(
        (medicine.id for medicine in medicines),
        default=0,
    ) + 1
    medicine = Medicine(medicine_id, name, dosage, unit)
    medicines.append(medicine)
    return medicine


def find_medicine(
    medicines: list[Medicine],
    query: str,
) -> list[Medicine]:
    """Ищет лекарства по названию."""
    query = query.lower()
    return [
        medicine
        for medicine in medicines
        if query in medicine.name.lower()
    ]


def filter_medicines_by_dosage(
    medicines: list[Medicine],
    min_dosage: int,
) -> list[Medicine]:
    """Отбирает лекарства с дозировкой не ниже указанной."""
    return [
        medicine
        for medicine in medicines
        if medicine.dosage >= min_dosage
    ]


def sort_medicines(medicines: list[Medicine]) -> list[Medicine]:
    """Сортирует лекарства по дозировке."""
    return sorted(medicines, key=lambda medicine: medicine.dosage)


def show_medicines(medicines: list[Medicine]) -> None:
    """Выводит лекарства."""
    if not medicines:
        print("Лекарств нет.")
        return
    for medicine in sort_medicines(medicines):
        print(medicine)
