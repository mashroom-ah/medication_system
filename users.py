def add_user(users: list[dict], name: str, age: int) -> dict:
    """Добавляет нового пользователя."""
    user_id = len(users) + 1

    user = {
        "id": user_id,
        "name": name,
        "age": age
    }

    users.append(user)
    return user


def find_user(users: list[dict], query: str) -> list[dict]:
    """Ищет пользователей по имени."""
    query = query.lower()

    return [
        user
        for user in users
        if query in user["name"].lower()
    ]


def sort_users(users: list[dict]) -> list[dict]:
    """Сортирует пользователей по возрасту."""
    return sorted(users, key=lambda user: user["age"])
