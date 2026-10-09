from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from ..exceptions import InvalidValueObject
from ..shared import EntityId

@dataclass(frozen=True)
class ScooterId(EntityId):
    pass
@dataclass(frozen=True)
class UserId(EntityId):
    pass
@dataclass(frozen=True)
class TripId(EntityId):
    pass
@dataclass(frozen=True)
class BatteryLevel:
    percent: int
    def __post_init__(self) -> None:
        if not isinstance(self.percent, int):
            raise InvalidValueObject("BatteryLevel.percent должен быть int")
        if not (0 <= self.percent <= 100):
            raise InvalidValueObject(
                f"Уровень заряда должен быть в диапазоне 0..100, получено {self.percent}"
            )
    def is_below(self, threshold: int) -> bool:
        return self.percent < threshold


@dataclass(frozen=True)
class Tariff:
    price_per_minute: Decimal
    minimum_price: Decimal

    def __post_init__(self) -> None:
        if self.price_per_minute < Decimal("0"):
            raise InvalidValueObject("Цена за минуту не может быть отрицательной")
        if self.minimum_price < Decimal("0"):
            raise InvalidValueObject("Минимальная стоимость не может быть отрицательной")

    def calculate(self, minutes: int) -> Decimal:
        if minutes < 0:
            raise InvalidValueObject("Длительность не может быть отрицательной")
        cost = self.price_per_minute * Decimal(minutes)
        return max(cost, self.minimum_price)