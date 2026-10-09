from __future__ import annotations

from uuid import uuid4

from ..exceptions import DomainInvariantViolation, EntityNotFound
from ..shared import TimeRange
from .booking import Booking, BookingStatus
from .repositories import BookingRepository, RoomRepository
from .value_objects import BookingId, EmployeeId, ParticipantCount, RoomId


class CreateBookingService:

    def __init__(
        self,
        room_repo: RoomRepository,
        booking_repo: BookingRepository,
    ) -> None:
        self._room_repo = room_repo
        self._booking_repo = booking_repo

    def create(
        self,
        room_id: RoomId,
        employee_id: EmployeeId,
        time_range: TimeRange,
        participants: ParticipantCount,
    ) -> Booking:
        room = self._room_repo.get(room_id)
        if room is None:
            raise EntityNotFound(f"Комната {room_id.value} не найдена")

        if participants.value > room.capacity.value:
            raise DomainInvariantViolation(
                f"Число участников {participants.value} превышает вместимость "
                f"комнаты {room.capacity.value}"
            )
        if not room.office_hours.contains(
            time_range.start.time(), time_range.end.time()
        ):
            raise DomainInvariantViolation(
            )
        for existing in self._booking_repo.find_active_by_room(room_id):
            if existing.time_range.overlaps(time_range):
                raise DomainInvariantViolation(
                    f"Бронь пересекается с существующей бронью {existing.id.value}"
                )
        booking = Booking(
            _id=BookingId(uuid4()),
            _room_id=room_id,
            _employee_id=employee_id,
            _time_range=time_range,
            _participants=participants,
        )
        self._booking_repo.add(booking)
        return booking