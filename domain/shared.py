from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Final
from uuid import UUID

from .exceptions import InvalidValueObject


@dataclass(frozen=True)
class EntityId:
    value: UUID

    def __post_init__(self) -> None:
        if not isinstance(self.value, UUID):
            raise InvalidValueObject("EntityId должен быть UUID")


@dataclass(frozen=True)
class TimeRange:
    start: datetime
    end: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.start, datetime) or not isinstance(self.end, datetime):
            raise InvalidValueObject("TimeRange принимает только datetime")
        if self.end < self.start:
            raise InvalidValueObject(
                "Конец интервала не может быть раньше начала"
            )

    def overlaps(self, other: "TimeRange") -> bool:
        return self.start < other.end and other.start < self.end

    def duration_minutes(self) -> int:
        delta = self.end - self.start
        return int(delta.total_seconds() // 60)

    def duration_hours_ceil(self) -> int:
        minutes = self.duration_minutes()
        if minutes <= 0:
            return 0
        return (minutes + 59) // 60


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: Final[str] = "RUB"

    def __post_init__(self) -> None:
        if not isinstance(self.amount, Decimal):
            raise InvalidValueObject("Money.amount должен быть Decimal")
        if self.amount < Decimal("0"):
            raise InvalidValueObject("Денежная сумма не может быть отрицательной")

    @classmethod
    def zero(cls) -> "Money":
        return cls(amount=Decimal("0"))

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise InvalidValueObject("Нельзя складывать разные валюты")
        return Money(amount=self.amount + other.amount)

    def __mul__(self, factor: int) -> "Money":
        return Money(amount=self.amount * Decimal(factor))