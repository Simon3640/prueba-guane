user_simon = {
    "id": 1,
    "username": "Simon0username",
    "names": "Simón",
    "last_names": "García Luján",
    "email": "simon.garcia@testing.com",
    "is_active": True,
    "is_superuser": False,
    "hashed_password": "Secret Hashed Password",
}

user_john = {
    "id": 2,
    "username": "John0username",
    "names": "John",
    "last_names": "David Gonzales",
    "email": "john.gonzales@testing.com",
    "is_active": True,
    "is_superuser": False,
    "hashed_password": "Secret Hashed Password",
}

user_simon_create = user_simon.copy()
user_simon_create["password"] = "Password create"

user_john_create = user_john.copy()
user_john_create["password"] = "Password create"

income_1 = {
    "id": 1,
    "name": "rent",
    "value": 1_000_000,
    "category_id": 1
}

income_2 = {
    "id": 2,
    "name": "food",
    "value": 500_000,
    "category_id": 1
}

category_1 = {
    "id": 2,
    "user_id": 1,
    "name": "Home",
    "category": [income_1, income_2]
}
