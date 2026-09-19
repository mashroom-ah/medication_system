from __future__ import annotations


class User:
    """Пользователь системы учёта лекарств."""

    def __init__(self, user_id: int, name: str, age: int) -> None:
        """Создаёт объект пользователя."""
        self.id = user_id
        self.name = name
        self.age = age

    def __str__(self) -> str:
        """Возвращает строковое представление пользователя."""
        return f"{self.name}, возраст: {self.age}, ID: {self.id}"

    @classmethod
    def from_data(cls, data: dict) -> User:
        """Создаёт пользователя из данных JSON."""
        return cls(
            user_id=int(data["id"]),
            name=str(data["name"]),
            age=int(data["age"]),
        )

    def to_data(self) -> dict:
        """Преобразует пользователя в структуру для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
        }


def add_user(users: list[User], name: str, age: int) -> User:
    """Создаёт пользователя и добавляет его в коллекцию."""
    user_id = max((user.id for user in users), default=0) + 1
    user = User(user_id, name, age)
    users.append(user)
    return user


def find_user(users: list[User], query: str) -> list[User]:
    """Ищет пользователей по имени."""
    query = query.lower()
    return [user for user in users if query in user.name.lower()]


def sort_users(users: list[User]) -> list[User]:
    """Сортирует пользователей по возрасту."""
    return sorted(users, key=lambda user: user.age)


def show_users(users: list[User]) -> None:
    """Выводит пользователей."""
    if not users:
        print("Пользователей нет.")
        return
    for user in sort_users(users):
        print(user)
