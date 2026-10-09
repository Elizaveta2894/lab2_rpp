from __future__ import annotations
from dataclasses import dataclass, field
from ..exceptions import DomainInvariantViolation
from .value_objects import BookId, ISBN

@dataclass
class Book:
    _id: BookId
    _title: str
    _isbn: ISBN
    _total_copies: int
    _available_copies: int = field(default=0)
    def __post_init__(self) -> None:
        if not self._title or not self._title.strip():
            raise DomainInvariantViolation("Название книги не может быть пустым")
        if self._total_copies <= 0:
            raise DomainInvariantViolation(
                "Общее количество экземпляров должно быть положительным"
            )
        if self._available_copies == 0:
            self._available_copies = self._total_copies
        if self._available_copies < 0:
            raise DomainInvariantViolation(
                "Количество доступных экземпляров не может быть отрицательным"
            )
        if self._available_copies > self._total_copies:
            raise DomainInvariantViolation(
                "Доступных экземпляров не может быть больше общего количества"
            )
    @property
    def id(self) -> BookId:
        return self._id
    @property
    def title(self) -> str:
        return self._title
    @property
    def isbn(self) -> ISBN:
        return self._isbn
    @property
    def total_copies(self) -> int:
        return self._total_copies
    @property
    def available_copies(self) -> int:
        return self._available_copies
    def is_available(self) -> bool:
        return self._available_copies > 0
    def lend_copy(self) -> None:
        if not self.is_available():
            raise DomainInvariantViolation(
                f"Нет свободных экземпляров книги {self._title!r}"
            )
        self._available_copies -= 1

    def return_copy(self) -> None:
        if self._available_copies >= self._total_copies:
            raise DomainInvariantViolation(
                "Нельзя вернуть экземпляр: все экземпляры уже в библиотеке"
            )
        self._available_copies += 1