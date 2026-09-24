"""Модели данных и интерфейсы источников.
Бот работает только с этими типами: любой источник (API, парсер, биржа)
подключается как адаптер, реализующий нужный Protocol."""
from dataclasses import dataclass
from typing import Protocol


@dataclass
class Match:
    id: str
    league: str
    home: str
    away: str
    start: str               # ISO-время начала
    status: str              # scheduled | live | finished
    score: str | None = None
    minute: int | None = None


@dataclass
class Odds:
    match_id: str
    bookmaker: str
    home: float
    draw: float
    away: float
    updated_at: str


@dataclass
class MoneyFlow:
    match_id: str
    source: str              # например "Betfair Exchange" - всегда показываем источник
    home_pct: float
    draw_pct: float
    away_pct: float
    volume: float | None     # общий объём, если известен
    updated_at: str


@dataclass
class Event:
    minute: int
    type: str                # goal | yellow | red | sub
    team: str
    player: str


@dataclass
class Lineup:
    team: str
    formation: str | None
    players: list[str]


@dataclass
class StandingRow:
    pos: int
    team: str
    played: int
    points: int
    goal_diff: int


class MatchProvider(Protocol):
    async def list_matches(self, live: bool) -> list[Match]: ...
    async def get_match(self, match_id: str) -> Match | None: ...
    async def get_events(self, match_id: str) -> list[Event]: ...
    async def get_lineups(self, match_id: str) -> list[Lineup]: ...
    async def get_standings(self, league: str) -> list[StandingRow]: ...


class OddsProvider(Protocol):
    async def get_odds(self, match_id: str) -> Odds | None: ...


class MoneyFlowProvider(Protocol):
    async def get_moneyflow(self, match_id: str) -> MoneyFlow | None: ...


@dataclass
class Providers:
    matches: MatchProvider
    odds: OddsProvider
    moneyflow: MoneyFlowProvider
