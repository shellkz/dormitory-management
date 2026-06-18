import os
import sqlite3
from datetime import datetime
from typing import Optional

from .models import Room, Stay, StayRead, User

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


# Helper
def current_datetime() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


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
    status: str | None = None,
    type: str | None = None,
    floor: int | None = None,
    id: int | None = None,
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
        if id is not None:
            conditions.append("id = ?")
            params.append(id)

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


## Stay
def check_in(username: str, room_id: int):
    # No such user
    user = get_user(username)
    if not user:
        raise ValueError(f"[Stay] No such user called {username}.")

    # No such room
    if not get_rooms(id=room_id):
        raise ValueError(f"[Stay] No such room id is {room_id}.")

    # Find latest stay record of room with given room_id
    latest_stay = get_latest_stay(room_id)

    # Someone not check out yet => someeone stay now => not available
    if latest_stay and latest_stay.check_out_at is None:
        raise ValueError("[Stay] Room is occupied.")

    # 1. No one ever check in this room => no one stay now => available
    # 2. Someone ever check in but no one currently check in this room => no one stay now => available

    # Check in
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO 
            Stay (resident_id, room_id, check_in_at) 
            VALUES (?, ?, ?) 
            """,
            (user.id, room_id, current_datetime()),
        )
        conn.commit()
    finally:
        if conn:
            conn.close()

    pass


def get_latest_stay(room_id: int) -> Stay | None:
    conn = None
    stay = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * 
            FROM Stay 
            WHERE room_id = ? 
            ORDER BY id DESC 
            LIMIT 1
            """,
            (room_id,),
        )
        stay = cursor.fetchone()
        if not stay:
            return None
        stay = Stay(**stay)
    finally:
        if conn:
            conn.close()
    return stay


# active_only = F, means stay history that are checked out.(Stay History)
# active_only = T, means stays that are checked in but not yet check out.(Ready for check out)
def get_stays(
    username: str | None = None,
    room_id: int | None = None,
    active_only: bool | None = None,
) -> list[StayRead]:
    ## Below conditions is true for my schema:
    ## 1. Room will get deleted in cascade manner
    ## 2. User won't get deleted
    ## Thus,
    ## Stay will always have matched Room and User
    ## I can use default INNER JOIN
    ## Instead of LEFT JOIN which assign null value to unmatched columns

    conn = None
    results = []
    try:
        conn = get_connection()
        cursor = conn.cursor()

        conditions = []
        params = []

        if username is not None:
            conditions.append("User.username = ?")
            params.append(username)

        if room_id is not None:
            conditions.append("Stay.room_id = ?")
            params.append(room_id)

        if active_only is not None:
            conditions.append(
                "Stay.check_out_at IS NULL"
                if active_only
                else "Stay.check_out_at IS NOT NULL"
            )

        sql = "SELECT Stay.resident_id, User.username, Stay.room_id, Room.type, Room.floor, Stay.check_in_at, Stay.check_out_at "
        sql += "FROM Stay "
        sql += "JOIN Room ON Stay.room_id = Room.id "
        sql += "JOIN User ON Stay.resident_id = User.id "
        if conditions:
            sql += "WHERE " + " AND ".join(conditions)
        sql += "ORDER BY Stay.id DESC "
        cursor.execute(sql, params)

        for stay in cursor.fetchall():
            results.append(StayRead(**stay))

    finally:
        if conn:
            conn.close()

    return results


def check_out(room_id: int):
    # No such room
    if not get_rooms(id=room_id):
        raise ValueError(f"[Stay] No such room id is {room_id}.")

    # No one stay at room with given room_id
    lastest_stay = get_latest_stay(room_id)
    ## 1. No one ever stayed
    if not lastest_stay:
        raise ValueError(f"[Stay] No one stay in room {room_id}.")
    ## 2. Lastest stay had checked out
    if lastest_stay.check_out_at is not None:
        raise ValueError(f"[Stay] No one stay in room {room_id}.")

    # check out
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE Stay 
            SET check_out_at = ? 
            WHERE id = ? 
            """,
            (
                current_datetime(),
                lastest_stay.id,
            ),
        )
        conn.commit()
    finally:
        if conn:
            conn.close()


# if __name__ == "__main__":
#   run_sql("001_create_db.sql")
#   run_sql("002_add_test_user.sql")
#   run_sql("003_add_test_room.sql")
