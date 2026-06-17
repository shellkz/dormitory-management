import os
import sqlite3
from typing import Optional

from .models import User

DATEBASE_NAME = "dorm.db"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_connection():
    db_path = os.path.join(BASE_DIR, DATEBASE_NAME)
    return sqlite3.connect(db_path)


# Run sql script unser db/scripts/
def run_sql(filename):
    filepath = os.path.join(BASE_DIR, "scripts", filename)
    conn = get_connection()
    with open(filepath, "r") as f:
        conn.executescript(f.read())
    conn.close()


# DB operation
## User
def get_user(username: str) -> Optional[User]:
    conn = None
    user = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User WHERE username = ?", (username,))
        user = cursor.fetchone()
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()
    return User(*user) if user else None


def create_user(username: str, password: str, role: str):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO User (username, password, role) VALUES (?, ?, ?)",
            (username, password, role),
        )
        conn.commit()
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()


# if __name__ == "__main__":
#     run_sql("001_create_db.sql")
#     run_sql("002_add_test_user.sql")
