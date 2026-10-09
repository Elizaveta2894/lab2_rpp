from __future__ import annotations

from dataclasses import dataclass
from datetime import time

from ..exceptions import InvalidValueObject
from ..shared import EntityId


@dataclass(frozen=True)
class RoomId(EntityId):
    pass


@dataclass(frozen=True)
class EmployeeId(EntityId):
    pass


@dataclass(frozen=True)
class BookingId(EntityId):
    pass

@dataclass(frozen=True)
class Capacity:
    value: int

    def __post_init__(self) -> None:
        if not isinstance(self.value, int):
            raise InvalidValueObject("Capacity должен быть int")
        if self.value <= 0:
            raise InvalidValueObject("Вместимость должна быть положительной")

@dataclass(frozen=True)
class ParticipantCount:
    value: int

    def __post_init__(self) -> None:
        if not isinstance(self.value, int):
            raise InvalidValueObject("ParticipantCount должен быть int")
        if self.value <= 0:
            raise InvalidValueObject("Число участников должно быть положительным")
@dataclass(frozen=True)
class OfficeHours:
    opens_at: time
    closes_at: time

    def __post_init__(self) -> None:
        if self.closes_at <= self.opens_at:
            raise InvalidValueObject(
                "Время закрытия должно быть позже времени открытия"
            )
    def contains(self, start: time, end: time) -> bool:
        return self.opens_at <= start and end <= self.closes_at