from __future__ import annotations
class DomainError(Exception):
    #Базовое исключение доменного слоя
    pass

class DomainInvariantViolation(DomainError):
    #Нарушение инварианта предметной области
    pass

class InvalidValueObject(DomainError):
    #Некорректное значение объекта-значения
    pass


class EntityNotFound(DomainError):
    #Сущность не найдена в репозитории
    pass