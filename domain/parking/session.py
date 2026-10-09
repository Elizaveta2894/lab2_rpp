from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from ..exceptions import DomainInvariantViolation
from ..shared import TimeRange
from .value_objects import (
    HourlyTariff,
    PlateNumber,
    SessionId,
    SpotId,
    VehicleId,
)

@dataclass
class ParkingSession:
    _id: SessionId
    _spot_id: SpotId
    _vehicle_id: VehicleId
    _plate: PlateNumber
    _time_range: TimeRange
    _tariff: HourlyTariff
    _closed: bool = False
    _cost: Optional[Decimal] = None

    @property
    def id(self) -> SessionId:
        return self._id
    @property
    def spot_id(self) -> SpotId:
        return self._spot_id
    @property
    def vehicle_id(self) -> VehicleId:
        return self._vehicle_id
    @property
    def plate(self) -> PlateNumber:
        return self._plate
    @property
    def time_range(self) -> TimeRange:
        return self._time_range
    @property
    def cost(self) -> Optional[Decimal]:
        return self._cost
    def is_closed(self) -> bool:
        return self._closed
    def close(self, exit_at: "datetime") -> Decimal:
        from datetime import datetime
        if self._closed:
            raise DomainInvariantViolation(
                f"Сессия {self._id.value} уже закрыта"
            )
        if exit_at < self._time_range.start:
            raise DomainInvariantViolation(
                "Время выезда не может быть раньше времени въезда"
            )

        new_range = TimeRange(start=self._time_range.start, end=exit_at)
        hours = new_range.duration_hours_ceil()
        cost = self._tariff.calculate(hours)

        self._time_range = new_range
        self._cost = cost
        self._closed = True
        return cost