from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from ..exceptions import InvalidValueObject
from ..shared import EntityId
@dataclass(frozen=True)
class SpotId(EntityId):
    pass
@dataclass(frozen=True)
class VehicleId(EntityId):
    pass
@dataclass(frozen=True)
class SessionId(EntityId):
    pass
class SpotStatus(str, Enum):
    FREE = "free"
    OCCUPIED = "occupied"

@dataclass(frozen=True)
class PlateNumber:
    value: str
    def __post_init__(self) -> None:
        cleaned = self.value.strip().upper()
        if len(cleaned) < 4 or len(cleaned) > 12:
            raise InvalidValueObject(
                f"Некорректный номер автомобиля: {self.value!r}"
            )
        object.__setattr__(self, "value", cleaned)


@dataclass(frozen=True)
class HourlyTariff:
    price_per_hour: Decimal

    def __post_init__(self) -> None:
        if self.price_per_hour < Decimal("0"):
            raise InvalidValueObject("Цена за час не может быть отрицательной")

    def calculate(self, hours_ceil: int) -> Decimal:
        if hours_ceil < 0:
            raise InvalidValueObject("Длительность не может быть отрицательной")
        return self.price_per_hour * Decimal(hours_ceil)