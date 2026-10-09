from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from ..exceptions import DomainInvariantViolation
from ..shared import TimeRange
from .value_objects import BookingId, EmployeeId, ParticipantCount, RoomId


class BookingStatus(str, Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"


@dataclass
class Booking:
    _id: BookingId
    _room_id: RoomId
    _employee_id: EmployeeId
    _time_range: TimeRange
    _participants: ParticipantCount
    _status: BookingStatus = BookingStatus.ACTIVE

    @property
    def id(self) -> BookingId:
        return self._id

    @property
    def room_id(self) -> RoomId:
        return self._room_id

    @property
    def employee_id(self) -> EmployeeId:
        return self._employee_id

    @property
    def time_range(self) -> TimeRange:
        return self._time_range

    @property
    def participants(self) -> ParticipantCount:
        return self._participants

    @property
    def status(self) -> BookingStatus:
        return self._status

    def cancel(self) -> None:
        if self._status == BookingStatus.CANCELLED:
            raise DomainInvariantViolation(
                f"Бронь {self._id.value} уже отменена"
            )
        self._status = BookingStatus.CANCELLED