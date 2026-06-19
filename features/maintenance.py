import db
from features.auth import is_username_valid
from features.room import is_id_valid

VALID_STATUS = {"submitted", "processing", "completed"}


def is_status_valid(status: str) -> bool:
    if status is None:
        return True
    return status in VALID_STATUS


def is_description_valid(description: str) -> bool:
    return bool(description and description.strip())


def submit_request(room_id: int, description: str, created_by: int):
    if not is_id_valid(room_id):
        raise ValueError(f"[Maintenance] Invalid room_id. Value = {room_id}")
    if not is_description_valid(description):
        raise ValueError(f"[Maintenance] Invalid description. Value = {description}")
    if not is_id_valid(created_by):
        raise ValueError(f"[Maintenance] Invalid created_by. Value = {created_by}")
    db.submit_request(room_id, description, created_by)


def process_request(id: int):
    if not is_id_valid(id):
        raise ValueError(f"[Maintenance] Invalid id. Value = {id}")
    db.process_maintenance_request(id)


def complete_request(id: int):
    if not is_id_valid(id):
        raise ValueError(f"[Maintenance] Invalid id. Value = {id}")
    db.complete_maintenance_request(id)


def get_requests(
    id: int | None = None,
    status: str | None = None,
    username: str | None = None,
    room_id: int | None = None,
) -> list[db.RequestMaintenanceRead]:
    if id is not None and not is_id_valid(id):
        raise ValueError(f"[Maintenance] Invalid id. Value = {id}")
    if not is_status_valid(status):
        raise ValueError(f"[Maintenance] Invalid status. Value = {status}")
    if username is not None and not is_username_valid(username):
        raise ValueError(f"[Maintenance] Invalid username. Value = {username}")
    if room_id is not None and not is_id_valid(room_id):
        raise ValueError(f"[Maintenance] Invalid room_id. Value = {room_id}")
    return db.get_maintenance_requests(id, status, username, room_id)
