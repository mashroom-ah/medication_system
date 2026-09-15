from datetime import datetime

from schedules import (
    add_schedule,
    is_schedule_due,
    sort_schedules,
)


def test_add_schedule():
    schedules = []

    schedule = add_schedule(
        schedules,
        1,
        1,
        12,
        0
    )

    assert schedule["id"] == 1
    assert schedule["user_id"] == 1
    assert schedule["medicine_id"] == 1
    assert schedule["hour"] == 12
    assert schedule["minute"] == 0


def test_is_schedule_due():
    schedule = {
        "id": 1,
        "user_id": 1,
        "medicine_id": 1,
        "hour": 12,
        "minute": 0
    }

    current_time = datetime(
        2026,
        9,
        13,
        12,
        30
    )

    assert is_schedule_due(
        schedule,
        current_time
    ) is True


def test_schedule_is_not_due():
    schedule = {
        "id": 1,
        "user_id": 1,
        "medicine_id": 1,
        "hour": 12,
        "minute": 0
    }

    current_time = datetime(
        2026,
        9,
        13,
        11,
        30
    )

    assert is_schedule_due(
        schedule,
        current_time
    ) is False


def test_sort_schedules():
    schedules = [
        {
            "id": 1,
            "hour": 18,
            "minute": 0
        },
        {
            "id": 2,
            "hour": 9,
            "minute": 30
        }
    ]

    result = sort_schedules(schedules)

    assert result[0]["hour"] == 9
    assert result[1]["hour"] == 18
