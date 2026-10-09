from __future__ import annotations

from typing import Dict, List, Optional

from domain.booking.booking import Booking
from domain.booking.repositories import BookingRepository, RoomRepository
from domain.booking.room import Room
from domain.booking.value_objects import BookingId, RoomId
from domain.library.book import Book
from domain.library.loan import Loan
from domain.library.repositories import BookRepository, LoanRepository
from domain.library.value_objects import BookId, LoanId, ReaderId
from domain.parking.repositories import (
    ParkingSessionRepository,
    ParkingSpotRepository,
)
from domain.parking.session import ParkingSession
from domain.parking.spot import ParkingSpot
from domain.parking.value_objects import SessionId, SpotId
from domain.scooter.repositories import ScooterRepository, TripRepository
from domain.scooter.scooter import Scooter
from domain.scooter.trip import Trip
from domain.scooter.value_objects import ScooterId, TripId

class InMemoryBookRepository(BookRepository):
    def __init__(self) -> None:
        self._storage: Dict[BookId, Book] = {}

    def get(self, book_id: BookId) -> Optional[Book]:
        return self._storage.get(book_id)

    def save(self, book: Book) -> None:
        self._storage[book.id] = book

    def add(self, book: Book) -> None:
        self._storage[book.id] = book

class InMemoryLoanRepository(LoanRepository):
    def __init__(self) -> None:
        self._storage: Dict[LoanId, Loan] = {}

    def get(self, loan_id: LoanId) -> Optional[Loan]:
        return self._storage.get(loan_id)

    def save(self, loan: Loan) -> None:
        self._storage[loan.id] = loan

    def add(self, loan: Loan) -> None:
        self._storage[loan.id] = loan

    def find_open_by_book_and_reader(
        self, book_id: BookId, reader_id: ReaderId
    ) -> Optional[Loan]:
        for loan in self._storage.values():
            if (
                loan.book_id == book_id
                and loan.reader_id == reader_id
                and not loan.is_closed()
            ):
                return loan
        return None

class InMemoryScooterRepository(ScooterRepository):
    def __init__(self) -> None:
        self._storage: Dict[ScooterId, Scooter] = {}

    def get(self, scooter_id: ScooterId) -> Optional[Scooter]:
        return self._storage.get(scooter_id)

    def save(self, scooter: Scooter) -> None:
        self._storage[scooter.id] = scooter

    def add(self, scooter: Scooter) -> None:
        self._storage[scooter.id] = scooter


class InMemoryTripRepository(TripRepository):
    def __init__(self) -> None:
        self._storage: Dict[TripId, Trip] = {}

    def get(self, trip_id: TripId) -> Optional[Trip]:
        return self._storage.get(trip_id)

    def save(self, trip: Trip) -> None:
        self._storage[trip.id] = trip

    def add(self, trip: Trip) -> None:
        self._storage[trip.id] = trip

class InMemoryRoomRepository(RoomRepository):
    def __init__(self) -> None:
        self._storage: Dict[RoomId, Room] = {}

    def get(self, room_id: RoomId) -> Optional[Room]:
        return self._storage.get(room_id)

    def add(self, room: Room) -> None:
        self._storage[room.id] = room


class InMemoryBookingRepository(BookingRepository):
    def __init__(self) -> None:
        self._storage: Dict[BookingId, Booking] = {}

    def get(self, booking_id: BookingId) -> Optional[Booking]:
        return self._storage.get(booking_id)

    def save(self, booking: Booking) -> None:
        self._storage[booking.id] = booking

    def add(self, booking: Booking) -> None:
        self._storage[booking.id] = booking

    def find_active_by_room(self, room_id: RoomId) -> List[Booking]:
        from domain.booking.booking import BookingStatus
        return [
            b
            for b in self._storage.values()
            if b.room_id == room_id and b.status == BookingStatus.ACTIVE
        ]

class InMemoryParkingSpotRepository(ParkingSpotRepository):
    def __init__(self) -> None:
        self._storage: Dict[SpotId, ParkingSpot] = {}

    def get(self, spot_id: SpotId) -> Optional[ParkingSpot]:
        return self._storage.get(spot_id)

    def save(self, spot: ParkingSpot) -> None:
        self._storage[spot.id] = spot

    def add(self, spot: ParkingSpot) -> None:
        self._storage[spot.id] = spot


class InMemoryParkingSessionRepository(ParkingSessionRepository):
    def __init__(self) -> None:
        self._storage: Dict[SessionId, ParkingSession] = {}

    def get(self, session_id: SessionId) -> Optional[ParkingSession]:
        return self._storage.get(session_id)

    def save(self, session: ParkingSession) -> None:
        self._storage[session.id] = session

    def add(self, session: ParkingSession) -> None:
        self._storage[session.id] = session