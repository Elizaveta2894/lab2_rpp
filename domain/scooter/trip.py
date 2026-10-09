from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from ..exceptions import DomainInvariantViolation
from ..shared import TimeRange
from .value_objects import ScooterId, Tariff, TripId, UserId

@dataclass
class Trip:
    _id: TripId
    _user_id: UserId
    _scooter_id: ScooterId
    _time_range: TimeRange
    _tariff: Tariff
    _finished: bool = False
    _cost: Optional[Decimal] = None
    @property
    def id(self) -> TripId:
        return self._id
    @property
    def user_id(self) -> UserId:
        return self._user_id
    @property
    def scooter_id(self) -> ScooterId:
        return self._scooter_id
    @property
    def time_range(self) -> TimeRange:
        return self._time_range
    @property
    def cost(self) -> Optional[Decimal]:
        return self._cost
    def is_finished(self) -> bool:
        return self._finished
    def finish(self) -> Decimal:
        if self._finished:
            raise DomainInvariantViolation(
                f"Поездка {self._id.value} уже завершена"
            )
        minutes = self._time_range.duration_minutes()
        cost = self._tariff.calculate(minutes)
        self._cost = cost
        self._finished = True
        return cost