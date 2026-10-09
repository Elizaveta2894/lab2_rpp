from datetime import date, datetime, time
from decimal import Decimal
from uuid import uuid4

from domain.booking.services import CreateBookingService
from domain.booking.value_objects import (
    Capacity,
    EmployeeId,
    OfficeHours,
    ParticipantCount,
    RoomId,
)
from domain.booking.room import Room
from domain.library.book import Book
from domain.library.services import IssueBookService, ReturnBookService
from domain.library.value_objects import BookId, ISBN, ReaderId
from domain.parking.services import FinishParkingService, StartParkingService
from domain.parking.value_objects import (
    HourlyTariff,
    PlateNumber,
    SpotId,
    VehicleId,
)
from domain.parking.spot import ParkingSpot
from domain.scooter.services import FinishTripService, StartTripService
from domain.scooter.value_objects import BatteryLevel, ScooterId, Tariff, UserId
from domain.scooter.scooter import Scooter
from domain.shared import TimeRange
from infrastructure.in_memory import (
    InMemoryBookingRepository,
    InMemoryBookRepository,
    InMemoryLoanRepository,
    InMemoryParkingSessionRepository,
    InMemoryParkingSpotRepository,
    InMemoryRoomRepository,
    InMemoryScooterRepository,
    InMemoryTripRepository,
)


def demo_library() -> None:
    print("=== Библиотека ===")
    book_repo = InMemoryBookRepository()
    loan_repo = InMemoryLoanRepository()

    book = Book(
        _id=BookId(uuid4()),
        _title="Domain-Driven Design",
        _isbn=ISBN("978-0321125217"),
        _total_copies=1,
    )
    book_repo.add(book)

    issue = IssueBookService(book_repo, loan_repo)
    return_service = ReturnBookService(book_repo, loan_repo, Decimal("50"))

    loan = issue.issue(
        book_id=book.id,
        reader_id=ReaderId(uuid4()),
        issued_at=date(2026, 1, 10),
        due_at=date(2026, 1, 24),
    )
    print(f"Выдана книга, доступно: {book.available_copies}")

    try:
        issue.issue(
            book_id=book.id,
            reader_id=ReaderId(uuid4()),
            issued_at=date(2026, 1, 11),
            due_at=date(2026, 1, 25),
        )
    except Exception as exc:
        print(f"Инвариант I1: {exc}")

    return_service.return_book(loan.id, date(2026, 1, 30))
    print(f"Возврат, доступно: {book.available_copies}, штраф: {loan.fine.amount}")


def demo_scooter() -> None:
    print("\n=== Прокат самокатов ===")
    scooter_repo = InMemoryScooterRepository()
    trip_repo = InMemoryTripRepository()

    scooter = Scooter(
        _id=ScooterId(uuid4()),
        _battery=BatteryLevel(80),
    )
    scooter_repo.add(scooter)

    start = StartTripService(scooter_repo, trip_repo, min_battery=20)
    finish = FinishTripService(scooter_repo, trip_repo)

    trip = start.start(
        scooter_id=scooter.id,
        user_id=UserId(uuid4()),
        started_at=datetime(2026, 1, 10, 12, 0),
        tariff=Tariff(
            price_per_minute=Decimal("5"),
            minimum_price=Decimal("50"),
        ),
    )
    print(f"Поездка начата, статус самоката: {scooter.status.value}")

    finish.finish(trip.id, datetime(2026, 1, 10, 12, 30))
    print(f"Поездка завершена, стоимость: {trip.cost}, статус: {scooter.status.value}")


def demo_booking() -> None:
    print("\n=== Бронирование переговорных ===")
    room_repo = InMemoryRoomRepository()
    booking_repo = InMemoryBookingRepository()

    room = Room(
        _id=RoomId(uuid4()),
        _name="Переговорная А",
        _capacity=Capacity(10),
        _office_hours=OfficeHours(opens_at=time(9, 0), closes_at=time(18, 0)),
    )
    room_repo.add(room)

    service = CreateBookingService(room_repo, booking_repo)

    booking = service.create(
        room_id=room.id,
        employee_id=EmployeeId(uuid4()),
        time_range=TimeRange(
            start=datetime(2026, 1, 10, 10, 0),
            end=datetime(2026, 1, 10, 11, 0),
        ),
        participants=ParticipantCount(5),
    )
    print(f"Бронь создана: {booking.id.value}")

    try:
        service.create(
            room_id=room.id,
            employee_id=EmployeeId(uuid4()),
            time_range=TimeRange(
                start=datetime(2026, 1, 10, 10, 30),
                end=datetime(2026, 1, 10, 11, 30),
            ),
            participants=ParticipantCount(3),
        )
    except Exception as exc:
        print(f"Инвариант пересечения: {exc}")


def demo_parking() -> None:
    print("\n=== Платная парковка ===")
    spot_repo = InMemoryParkingSpotRepository()
    session_repo = InMemoryParkingSessionRepository()

    spot = ParkingSpot(_id=SpotId(uuid4()), _number="A-01")
    spot_repo.add(spot)

    start = StartParkingService(spot_repo, session_repo)
    finish = FinishParkingService(spot_repo, session_repo)

    session = start.start(
        spot_id=spot.id,
        vehicle_id=VehicleId(uuid4()),
        plate=PlateNumber("А123ВС"),
        entry_at=datetime(2026, 1, 10, 10, 0),
        tariff=HourlyTariff(price_per_hour=Decimal("100")),
    )
    print(f"Сессия начата, место: {spot.status.value}")

    finish.finish(session.id, datetime(2026, 1, 10, 12, 30))
    print(f"Сессия закрыта, стоимость: {session.cost}, место: {spot.status.value}")


if __name__ == "__main__":
    demo_library()
    demo_scooter()
    demo_booking()
    demo_parking()