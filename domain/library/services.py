from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import uuid4
from ..exceptions import EntityNotFound
from .book import Book
from .loan import Loan
from .repositories import BookRepository, LoanRepository
from .value_objects import BookId, LoanId, LoanPeriod, ReaderId

class IssueBookService:
    def __init__(self, book_repo: BookRepository, loan_repo: LoanRepository) -> None:
        self._book_repo = book_repo
        self._loan_repo = loan_repo

    def issue(
        self,
        book_id: BookId,
        reader_id: ReaderId,
        issued_at: date,
        due_at: date,
    ) -> Loan:
        book = self._book_repo.get(book_id)
        if book is None:
            raise EntityNotFound(f"Книга {book_id.value} не найдена")

        book.lend_copy()
        self._book_repo.save(book)

        loan = Loan(
            _id=LoanId(uuid4()),
            _reader_id=reader_id,
            _book_id=book_id,
            _period=LoanPeriod(issued_at=issued_at, due_at=due_at),
        )
        self._loan_repo.add(loan)
        return loan


class ReturnBookService:

    def __init__(
        self,
        book_repo: BookRepository,
        loan_repo: LoanRepository,
        fine_per_day: Decimal,
    ) -> None:
        self._book_repo = book_repo
        self._loan_repo = loan_repo
        self._fine_per_day = fine_per_day

    def return_book(self, loan_id: LoanId, returned_at: date) -> None:
        loan = self._loan_repo.get(loan_id)
        if loan is None:
            raise EntityNotFound(f"Выдача {loan_id.value} не найдена")

        loan.close(returned_at=returned_at, fine_per_day=self._fine_per_day)
        self._loan_repo.save(loan)

        book = self._book_repo.get(loan.book_id)
        if book is None:
            raise EntityNotFound(f"Книга {loan.book_id.value} не найдена")
        book.return_copy()
        self._book_repo.save(book)