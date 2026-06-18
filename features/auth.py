import re

from db import User, create_user, get_user
from utils import hash


def is_username_valid(username: str) -> bool:
    # string consist of at 5 alphabets and digits.
    return bool(re.match(r"^[a-zA-Z0-9]{5,}$", username))


def is_password_valid(password: str) -> bool:
    return is_username_valid(password)


def login(username: str, password: str) -> User:
    if not is_username_valid(username):
        raise ValueError("[Auth] Invalid username.")
    if not is_password_valid(password):
        raise ValueError("[Auth] Invalid password.")

    user = get_user(username)

    if not user:
        raise ValueError("[Auth] No such username exists.")

    actual_password = user.password
    if hash(password) != actual_password:
        raise ValueError("[Auth] Password is incorrect.")
    return user


def register(username: str, password: str):
    if not is_username_valid(username):
        raise ValueError("[Auth] Invalid username.")
    if not is_password_valid(password):
        raise ValueError("[Auth] Invalid password.")

    user = get_user(username)

    if user:
        raise ValueError("[Auth] Username already exists.")

    # insert
    create_user(username, hash(password), "resident")


# python -m features.auth
if __name__ == "__main__":
    try:
        register("caster1078", "password")
        # user = login("caster1078", "password")
        # print(user)
    except Exception as e:
        print(e)
