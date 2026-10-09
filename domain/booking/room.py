from __future__ import annotations
from dataclasses import dataclass
from .value_objects import Capacity, OfficeHours, RoomId

@dataclass
class Room:
    _id: RoomId
    _name: str
    _capacity: Capacity
    _office_hours: OfficeHours

    @property
    def id(self) -> RoomId:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def capacity(self) -> Capacity:
        return self._capacity

    @property
    def office_hours(self) -> OfficeHours:
        return self._office_hours