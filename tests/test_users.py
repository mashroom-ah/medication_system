from users import add_user, find_user, sort_users


def test_add_user():
    users = []

    user = add_user(
        users,
        "Котов Кирилл",
        19
    )

    assert user["id"] == 1
    assert user["name"] == "Котов Кирилл"
    assert user["age"] == 19


def test_find_user():
    users = [
        {
            "id": 1,
            "name": "Новикова Мария",
            "age": 19
        },
        {
            "id": 2,
            "name": "Иванов Иван",
            "age": 25
        }
    ]

    result = find_user(users, "мария")

    assert len(result) == 1
    assert result[0]["name"] == "Новикова Мария"


def test_sort_users():
    users = [
        {
            "id": 1,
            "name": "Иван",
            "age": 30
        },
        {
            "id": 2,
            "name": "Мария",
            "age": 19
        }
    ]

    result = sort_users(users)

    assert result[0]["age"] == 19
    assert result[1]["age"] == 30
