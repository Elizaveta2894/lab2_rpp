from __future__ import annotations
from dataclasses import dataclass
from ..exceptions import DomainInvariantViolation
from .value_objects import SpotId, SpotStatus
@dataclass
class ParkingSpot:
    _id: SpotId
    _number: str
    _status: SpotStatus = SpotStatus.FREE
    @property
    def id(self) -> SpotId:
        return self._id
    @property
    def number(self) -> str:
        return self._number
    @property
    def status(self) -> SpotStatus:
        return self._status
    def occupy(self) -> None:
        if self._status == SpotStatus.OCCUPIED:
            raise DomainInvariantViolation(
                f"Место {self._number} уже занято"
            )
        self._status = SpotStatus.OCCUPIED
    def release(self) -> None:
        if self._status == SpotStatus.FREE:
            raise DomainInvariantViolation(
                f"Место {self._number} уже свободно"
            )
        self._status = SpotStatus.FREE