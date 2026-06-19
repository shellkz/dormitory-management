import db

VALID_STATUS = {"available", "occupied"}
VALID_TYPE = {"small", "medium", "large"}


def is_status_valid(status: str) -> bool:
    if status is None:
        return True
    return status in VALID_STATUS


def is_type_valid(type: str) -> bool:
    if type is None:
        return True
    return type in VALID_TYPE


def is_floor_valid(floor: int) -> bool:
    if floor is None:
        return True
    return floor > 0


def is_id_valid(id: int) -> bool:
    return id >= 0


def get_rooms(
    status: str | None = None, _type: str | None = None, floor: int | None = None
) -> list[db.RoomRead]:
    if not is_status_valid(status):
        raise ValueError("[Room] Invalid status value.")
    if not is_type_valid(_type):
        raise ValueError("[Room] Invalid type value.")
    if not is_floor_valid(floor):
        raise ValueError("[Room] Invalid floor value.")

    return db.get_rooms(status, _type, floor)


def create_room(type: str, floor: int):
    if not is_type_valid(type):
        raise ValueError(f"[Room] Invalid type value. Value = {type}")
    if not is_floor_valid(floor):
        raise ValueError(f"[Room] Invalid floor value. Value = {floor}")
    db.create_room(type, floor)


def delete_room(id: int):
    if not is_id_valid(id):
        raise ValueError(f"[Room] Invalid id value. Value = {id}")
    db.delete_room(id)


def update_room(id: int, type: str, floor: int):
    if not is_id_valid(id):
        raise ValueError(f"[Room] Invalid id value. Value = {id}")
    if not is_type_valid(type):
        raise ValueError(f"[Room] Invalid type value. Value = {type}")
    if not is_floor_valid(floor):
        raise ValueError(f"[Room] Invalid floor value. Value = {floor}")
    db.update_room(id, type, floor)
