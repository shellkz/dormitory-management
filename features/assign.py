import db
from features.auth import is_username_valid
from features.room import is_id_valid


def check_in(username: str, room_id: int):
    if not is_username_valid(username):
        raise ValueError(f"[Stay] Invalid username. Value = {username}")
    if not is_id_valid(room_id):
        raise ValueError(f"[Stay] Invalid room_id. Value = {room_id}")
    db.check_in(username, room_id)


def check_out(room_id: int):
    if not is_id_valid(room_id):
        raise ValueError(f"[Stay] Invalid room_id. Value = {room_id}")
    db.check_out(room_id)


def get_stays(
    username: str | None = None,
    room_id: int | None = None,
    active_only: bool | None = None,
) -> list[db.StayRead]:
    if username is not None and not is_username_valid(username):
        raise ValueError(f"[Stay] Invalid username. Value = {username}")
    if room_id is not None and not is_id_valid(room_id):
        raise ValueError(f"[Stay] Invalid room_id. Value = {room_id}")
    return db.get_stays(username, room_id, active_only)
