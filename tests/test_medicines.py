from medicines import (
    add_medicine,
    filter_medicines_by_dosage,
    find_medicine,
    sort_medicines,
)


def test_add_medicine():
    medicines = []

    medicine = add_medicine(
        medicines,
        "Парацетамол",
        500,
        "мг"
    )

    assert medicine["id"] == 1
    assert medicine["name"] == "Парацетамол"
    assert medicine["dosage"] == 500


def test_find_medicine():
    medicines = [
        {
            "id": 1,
            "name": "Аскорбиновая кислота",
            "dosage": 10,
            "unit": "мг"
        },
        {
            "id": 2,
            "name": "Парацетамол",
            "dosage": 500,
            "unit": "мг"
        }
    ]

    result = find_medicine(
        medicines,
        "парацетамол"
    )

    assert len(result) == 1
    assert result[0]["id"] == 2


def test_filter_medicines_by_dosage():
    medicines = [
        {
            "id": 1,
            "name": "Витамин C",
            "dosage": 10,
            "unit": "мг"
        },
        {
            "id": 2,
            "name": "Парацетамол",
            "dosage": 500,
            "unit": "мг"
        }
    ]

    result = filter_medicines_by_dosage(
        medicines,
        100
    )

    assert len(result) == 1
    assert result[0]["name"] == "Парацетамол"


def test_sort_medicines():
    medicines = [
        {
            "id": 1,
            "name": "Парацетамол",
            "dosage": 500,
            "unit": "мг"
        },
        {
            "id": 2,
            "name": "Витамин C",
            "dosage": 10,
            "unit": "мг"
        }
    ]

    result = sort_medicines(medicines)

    assert result[0]["dosage"] == 10
    assert result[1]["dosage"] == 500
