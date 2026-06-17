#   Disclosure:
#       I defined db schema by myself, and let AI generate model objects boilerplate.
#       I think this is fair usage.
from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    id: int
    username: str
    password: str
    role: str


@dataclass
class Room:
    id: int
    type: str
    floor: int


@dataclass
class Stay:
    id: int
    resident_id: int
    room_id: int
    check_in_at: str
    check_out_at: Optional[str]


@dataclass
class RequestMaintenance:
    id: int
    created_by: int
    room_id: int
    status: str
    description: str
    created_at: str
    processing_at: Optional[str]
    completed_at: Optional[str]
