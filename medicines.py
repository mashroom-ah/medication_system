def add_medicine(
        medicines: list[dict],
        name: str,
        dosage: int,
        unit: str
) -> dict:
    """Добавляет новое лекарство."""
    medicine_id = len(medicines) + 1

    medicine = {
        "id": medicine_id,
        "name": name,
        "dosage": dosage,
        "unit": unit
    }

    medicines.append(medicine)
    return medicine


def find_medicine(
        medicines: list[dict],
        query: str
) -> list[dict]:
    """Ищет лекарства по названию."""
    query = query.lower()

    return [
        medicine
        for medicine in medicines
        if query in medicine["name"].lower()
    ]


def filter_medicines_by_dosage(
        medicines: list[dict],
        min_dosage: int
) -> list[dict]:
    """Возвращает лекарства с дозировкой не меньше заданной."""
    return [
        medicine
        for medicine in medicines
        if min_dosage <= medicine["dosage"]
    ]


def sort_medicines(medicines: list[dict]) -> list[dict]:
    """Сортирует лекарства по дозировке."""
    return sorted(
        medicines,
        key=lambda medicine: medicine["dosage"]
    )
