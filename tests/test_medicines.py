from models.medicines import (
    Medicine,
    add_medicine,
    filter_medicines_by_dosage,
    find_medicine,
    sort_medicines,
)


def test_medicine_constructor_and_str() -> None:
    medicine = Medicine(1, "Парацетамол", 500, "мг")
    assert medicine.id == 1
    assert "Парацетамол" in str(medicine)


def test_add_medicine() -> None:
    medicines: list[Medicine] = []
    medicine = add_medicine(medicines, "Парацетамол", 500, "мг")
    assert medicine.id == 1
    assert medicine.dosage == 500


def test_find_medicine() -> None:
    medicines = [
        Medicine(1, "Аскорбиновая кислота", 10, "мг"),
        Medicine(2, "Парацетамол", 500, "мг"),
    ]
    result = find_medicine(medicines, "парацетамол")
    assert len(result) == 1
    assert result[0].id == 2


def test_filter_and_sort_medicines() -> None:
    medicines = [
        Medicine(1, "Парацетамол", 500, "мг"),
        Medicine(2, "Витамин C", 10, "мг"),
    ]
    filtered = filter_medicines_by_dosage(medicines, 100)
    sorted_medicines = sort_medicines(medicines)
    assert len(filtered) == 1
    assert sorted_medicines[0].dosage == 10
