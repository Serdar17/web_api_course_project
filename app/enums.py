from enum import Enum


class Status(str, Enum):
    Active = "ACTIVE"
    Pending = "PENDING"
    Completed = "COMPLETED"
