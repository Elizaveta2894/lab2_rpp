from __future__ import annotations
from datetime import datetime
from uuid import uuid4
from ..exceptions import EntityNotFound
from ..shared import TimeRange
from .repositories import ParkingSessionRepository, ParkingSpotRepository
from .session import ParkingSession
from .value_objects import (
    HourlyTariff,
    PlateNumber,
    SessionId,
    SpotId,
    VehicleId,
)
class StartParkingService:

    def __init__(
        self,
        spot_repo: ParkingSpotRepository,
        session_repo: ParkingSessionRepository,
    ) -> None:
        self._spot_repo = spot_repo
        self._session_repo = session_repo

    def start(
        self,
        spot_id: SpotId,
        vehicle_id: VehicleId,
        plate: PlateNumber,
        entry_at: datetime,
        tariff: HourlyTariff,
    ) -> ParkingSession:
        spot = self._spot_repo.get(spot_id)
        if spot is None:
            raise EntityNotFound(f"Место {spot_id.value} не найдено")

        spot.occupy()
        self._spot_repo.save(spot)

        session = ParkingSession(
            _id=SessionId(uuid4()),
            _spot_id=spot_id,
            _vehicle_id=vehicle_id,
            _plate=plate,
            _time_range=TimeRange(start=entry_at, end=entry_at),
            _tariff=tariff,
        )
        self._session_repo.add(session)
        return session

class FinishParkingService:

    def __init__(
        self,
        spot_repo: ParkingSpotRepository,
        session_repo: ParkingSessionRepository,
    ) -> None:
        self._spot_repo = spot_repo
        self._session_repo = session_repo

    def finish(self, session_id: SessionId, exit_at: datetime) -> None:
        session = self._session_repo.get(session_id)
        if session is None:
            raise EntityNotFound(f"Сессия {session_id.value} не найдена")

        session.close(exit_at)
        self._session_repo.save(session)

        spot = self._spot_repo.get(session.spot_id)
        if spot is None:
            raise EntityNotFound(f"Место {session.spot_id.value} не найдено")
        spot.release()
        self._spot_repo.save(spot)