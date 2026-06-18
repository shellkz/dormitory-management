import os
import sqlite3
from typing import Optional

from .models import Room, User

DATEBASE_NAME = "dorm.db"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_connection():
    db_path = os.path.join(BASE_DIR, DATEBASE_NAME)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


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
    finally:
        if conn:
            conn.close()
    return User(**user) if user else None


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
    finally:
        if conn:
            conn.close()


## Room


## Todo: Not yet implemented status filter, need to join table
def get_rooms(
    status: str | None = None, type: str | None = None, floor: int | None = None
) -> list[Room]:
    conn = None
    result: list[Room] = []
    try:
        conn = get_connection()
        cursor = conn.cursor()

        conditions = []
        params = []

        # if status is not None:
        #     conditions.append("status = ?")
        #     params.append(status)
        if type is not None:
            conditions.append("type = ?")
            params.append(type)
        if floor is not None:
            conditions.append("floor = ?")
            params.append(floor)

        sql = "SELECT * FROM Room "
        if conditions:
            sql += "WHERE " + " AND ".join(conditions)
        cursor.execute(sql, params)
        for room in cursor.fetchall():
            result.append(Room(**room))
    finally:
        if conn:
            conn.close()
    return result


def create_room(type: str, floor: int):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Room (type, floor) VALUES (?, ?)",
            (type, floor),
        )
        conn.commit()
    finally:
        if conn:
            conn.close()


def delete_room(id: int):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM Room WHERE id = ?",
            (id,),
        )
        if cursor.rowcount == 0:
            raise ValueError(f"[Room] Room {id} doesn't exist.")
        conn.commit()
    finally:
        if conn:
            conn.close()


def update_room(id: int, type: str | None = None, floor: int | None = None):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        conditions = []
        params = []

        if type is not None:
            conditions.append("type = ?")
            params.append(type)
        if floor is not None:
            conditions.append("floor = ?")
            params.append(floor)
        params.append(id)

        if not conditions:
            raise ValueError(
                "[Room] Update room should at least provide type or floor."
            )

        sql = "UPDATE Room "
        sql += "SET " + " , ".join(conditions)
        sql += " WHERE id = ?"
        cursor.execute(sql, params)

        if cursor.rowcount == 0:
            raise ValueError(f"[Room] Room {id} doesn't exist.")
        conn.commit()
    finally:
        if conn:
            conn.close()


# if __name__ == "__main__":
#   run_sql("001_create_db.sql")
#   run_sql("002_add_test_user.sql")
#   run_sql("003_add_test_room.sql")
