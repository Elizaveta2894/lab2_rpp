from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from ..exceptions import DomainInvariantViolation
from .value_objects import BatteryLevel, ScooterId

class ScooterStatus(str, Enum):
    FREE = "free"
    RENTED = "rented"
    MAINTENANCE = "maintenance"
@dataclass
class Scooter:
    _id: ScooterId
    _battery: BatteryLevel
    _status: ScooterStatus = ScooterStatus.FREE
    @property
    def id(self) -> ScooterId:
        return self._id
    @property
    def battery(self) -> BatteryLevel:
        return self._battery

    @property
    def status(self) -> ScooterStatus:
        return self._status
    def is_available(self, min_battery: int) -> bool:
        return (
            self._status == ScooterStatus.FREE
            and not self._battery.is_below(min_battery)
        )
    def rent(self, min_battery: int) -> None:
        if self._status != ScooterStatus.FREE:
            raise DomainInvariantViolation(
                f"Самокат {self._id.value} не свободен: {self._status.value}"
            )
        if self._battery.is_below(min_battery):
            raise DomainInvariantViolation(
                f"Заряд {self._battery.percent}% ниже минимального порога {min_battery}%"
            )
        self._status = ScooterStatus.RENTED

    def return_to_free(self) -> None:
        if self._status != ScooterStatus.RENTED:
            raise DomainInvariantViolation(
                "Вернуть в свободные можно только арендованный самокат"
            )
        self._status = ScooterStatus.FREE

    def send_to_maintenance(self) -> None:
        if self._status == ScooterStatus.RENTED:
            raise DomainInvariantViolation(
                "Нельзя отправить на обслуживание арендованный самокат"
            )
        self._status = ScooterStatus.MAINTENANCE