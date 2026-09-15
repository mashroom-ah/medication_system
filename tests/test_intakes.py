from intakes import (
    cancel_intake,
    create_intake,
    get_intakes_by_date,
    is_medicine_taken,
)


def test_create_intake():
    intakes = []

    intake = create_intake(
        intakes,
        1,
        "2026-09-13"
    )

    assert intake["id"] == 1
    assert intake["schedule_id"] == 1
    assert intake["date"] == "2026-09-13"
    assert intake["taken"] is True


def test_is_medicine_taken_for_date():
    intakes = [
        {
            "id": 1,
            "schedule_id": 1,
            "date": "2026-09-13",
            "taken": True
        }
    ]

    assert is_medicine_taken(
        intakes,
        1,
        "2026-09-13"
    ) is True


def test_medicine_not_taken_on_another_date():
    intakes = [
        {
            "id": 1,
            "schedule_id": 1,
            "date": "2026-09-13",
            "taken": True
        }
    ]

    assert is_medicine_taken(
        intakes,
        1,
        "2026-09-14"
    ) is False


def test_cancel_intake():
    intakes = [
        {
            "id": 1,
            "schedule_id": 1,
            "date": "2026-09-13",
            "taken": True
        }
    ]

    result = cancel_intake(
        intakes,
        1,
        "2026-09-13"
    )

    assert result is True
    assert intakes == []


def test_get_intakes_by_date():
    intakes = [
        {
            "id": 1,
            "schedule_id": 1,
            "date": "2026-09-13",
            "taken": True
        },
        {
            "id": 2,
            "schedule_id": 1,
            "date": "2026-09-14",
            "taken": True
        }
    ]

    result = get_intakes_by_date(
        intakes,
        "2026-09-13"
    )

    assert len(result) == 1
    assert result[0]["id"] == 1
