from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID
from ..exceptions import InvalidValueObject
from ..shared import EntityId

@dataclass(frozen=True)
class BookId(EntityId):
    pass

@dataclass(frozen=True)
class ReaderId(EntityId):
    pass
@dataclass(frozen=True)
class LoanId(EntityId):
    pass
@dataclass(frozen=True)
class ISBN:
    value: str

    def __post_init__(self) -> None:
        cleaned = self.value.replace("-", "").strip()
        if len(cleaned) not in (10, 13) or not cleaned.isdigit():
            raise InvalidValueObject(
                f"ISBN должен содержать 10 или 13 цифр, получено: {self.value!r}"
            )
        object.__setattr__(self, "value", cleaned)


@dataclass(frozen=True)
class LoanPeriod:
    issued_at: date
    due_at: date

    def __post_init__(self) -> None:
        if not isinstance(self.issued_at, date) or not isinstance(self.due_at, date):
            raise InvalidValueObject("LoanPeriod принимает только date")
        if self.due_at < self.issued_at:
            raise InvalidValueObject(
                "Срок возврата не может быть раньше даты выдачи"
            )

    def is_overdue(self, returned_at: date) -> bool:
        return returned_at > self.due_at

    def overdue_days(self, returned_at: date) -> int:
        if not self.is_overdue(returned_at):
            return 0
        return (returned_at - self.due_at).days


@dataclass(frozen=True)
class Fine:
    amount: Decimal
    currency: str = "RUB"

    def __post_init__(self) -> None:
        if not isinstance(self.amount, Decimal):
            raise InvalidValueObject("Fine.amount должен быть Decimal")
        if self.amount < Decimal("0"):
            raise InvalidValueObject("Сумма штрафа не может быть отрицательной")

    @classmethod
    def zero(cls) -> "Fine":
        return cls(amount=Decimal("0"))