from __future__ import annotations
from datetime import datetime
from uuid import uuid4
from ..exceptions import EntityNotFound
from ..shared import TimeRange
from .repositories import ScooterRepository, TripRepository
from .trip import Trip
from .value_objects import ScooterId, Tariff, TripId, UserId


class StartTripService:
    def __init__(
        self,
        scooter_repo: ScooterRepository,
        trip_repo: TripRepository,
        min_battery: int,
    ) -> None:
        self._scooter_repo = scooter_repo
        self._trip_repo = trip_repo
        self._min_battery = min_battery

    def start(
        self,
        scooter_id: ScooterId,
        user_id: UserId,
        started_at: datetime,
        tariff: Tariff,
    ) -> Trip:
        scooter = self._scooter_repo.get(scooter_id)
        if scooter is None:
            raise EntityNotFound(f"Самокат {scooter_id.value} не найден")

        scooter.rent(self._min_battery)
        self._scooter_repo.save(scooter)

        trip = Trip(
            _id=TripId(uuid4()),
            _user_id=user_id,
            _scooter_id=scooter_id,
            _time_range=TimeRange(start=started_at, end=started_at),
            _tariff=tariff,
        )
        self._trip_repo.add(trip)
        return trip

class FinishTripService:
    def __init__(
        self,
        scooter_repo: ScooterRepository,
        trip_repo: TripRepository,
    ) -> None:
        self._scooter_repo = scooter_repo
        self._trip_repo = trip_repo

    def finish(self, trip_id: TripId, finished_at: datetime) -> None:
        trip = self._trip_repo.get(trip_id)
        if trip is None:
            raise EntityNotFound(f"Поездка {trip_id.value} не найдена")

        if finished_at < trip.time_range.start:
            from ..exceptions import DomainInvariantViolation
            raise DomainInvariantViolation(
                "Время окончания поездки не может быть раньше времени начала"
            )
        trip._time_range = TimeRange(start=trip.time_range.start, end=finished_at)
        trip.finish()
        self._trip_repo.save(trip)

        scooter = self._scooter_repo.get(trip.scooter_id)
        if scooter is None:
            raise EntityNotFound(f"Самокат {trip.scooter_id.value} не найден")
        scooter.return_to_free()
        self._scooter_repo.save(scooter)