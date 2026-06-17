import re

from db import User, create_user, get_user
from utils import hash


def isUsernameValid(username: str) -> bool:
    # string consist of at 5 alphabets and digits.
    return bool(re.match(r"^[a-zA-Z0-9]{5,}$", username))


def ispasswordValid(password: str) -> bool:
    return isUsernameValid(password)


def login(username: str, password: str) -> User:
    if not isUsernameValid(username):
        raise ValueError("[Auth] Invalid username.")
    if not ispasswordValid(password):
        raise ValueError("[Auth] Invalid password.")

    user = get_user(username)

    if not user:
        raise ValueError("[Auth] No such username exists.")

    actual_password = user.password
    if hash(password) != actual_password:
        raise ValueError("[Auth] Password is incorrect.")
    return user


def register(username: str, password: str):
    if not isUsernameValid(username):
        raise ValueError("[Auth] Invalid username.")
    if not ispasswordValid(password):
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
