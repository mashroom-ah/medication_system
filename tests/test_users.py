from models.users import User, add_user, find_user, sort_users


def test_user_constructor_and_str() -> None:
    user = User(1, "Иванов Иван", 25)
    assert user.id == 1
    assert "Иванов Иван" in str(user)


def test_add_user() -> None:
    users: list[User] = []
    user = add_user(users, "Иванов Иван", 25)
    assert user.id == 1
    assert users == [user]


def test_find_user() -> None:
    users = [
        User(1, "Новикова Мария", 19),
        User(2, "Иванов Иван", 25),
    ]
    result = find_user(users, "мария")
    assert len(result) == 1
    assert result[0].name == "Новикова Мария"


def test_sort_users() -> None:
    users = [User(1, "Иван", 30), User(2, "Мария", 19)]
    result = sort_users(users)
    assert result[0].age == 19
