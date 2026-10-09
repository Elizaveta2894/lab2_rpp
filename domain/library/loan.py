from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

from ..exceptions import DomainInvariantViolation
from .value_objects import BookId, Fine, LoanId, LoanPeriod, ReaderId


@dataclass
class Loan:
    _id: LoanId
    _reader_id: ReaderId
    _book_id: BookId
    _period: LoanPeriod
    _returned_at: Optional[date] = None
    _fine: Optional[Fine] = None

    def __post_init__(self) -> None:
        if self._returned_at is not None and self._returned_at < self._period.issued_at:
            raise DomainInvariantViolation(
                "Дата возврата не может быть раньше даты выдачи"
            )

    @property
    def id(self) -> LoanId:
        return self._id
    @property
    def reader_id(self) -> ReaderId:
        return self._reader_id
    @property
    def book_id(self) -> BookId:
        return self._book_id
    @property
    def period(self) -> LoanPeriod:
        return self._period
    @property
    def returned_at(self) -> Optional[date]:
        return self._returned_at
    @property
    def fine(self) -> Optional[Fine]:
        return self._fine
    def is_closed(self) -> bool:
        return self._returned_at is not None
    def close(self, returned_at: date, fine_per_day: Decimal) -> Fine:
        if self.is_closed():
            raise DomainInvariantViolation(
                f"Выдача {self._id.value} уже закрыта"
            )
        if returned_at < self._period.issued_at:
            raise DomainInvariantViolation(
                "Дата возврата не может быть раньше даты выдачи"
            )

        overdue_days = self._period.overdue_days(returned_at)
        amount = fine_per_day * overdue_days
        fine = Fine(amount=amount)

        self._returned_at = returned_at
        self._fine = fine
        return fine