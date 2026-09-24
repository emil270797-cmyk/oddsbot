"""Заглушка с ТЕСТОВЫМИ данными, чтобы бот запускался без API.
Замените на реальные адаптеры, реализующие те же методы."""
from datetime import datetime, timezone
from .base import (Match, Odds, MoneyFlow, Event, Lineup, StandingRow)

NOW = lambda: datetime.now(timezone.utc).strftime("%H:%M:%S UTC")

_MATCHES = [
    Match("1", "Тест-лига", "Команда A", "Команда B", "2026-09-24T19:00:00Z", "scheduled"),
    Match("2", "Тест-лига", "Команда C", "Команда D", "2026-09-24T17:00:00Z", "live", "1:0", 63),
]


class StubMatches:
    async def list_matches(self, live: bool):
        return [m for m in _MATCHES if (m.status == "live") == live]

    async def get_match(self, match_id):
        return next((m for m in _MATCHES if m.id == match_id), None)

    async def get_events(self, match_id):
        return [Event(27, "goal", "Команда C", "Игрок 9")] if match_id == "2" else []

    async def get_lineups(self, match_id):
        return [Lineup("Хозяева", "4-3-3", ["Игрок 1", "Игрок 2", "Игрок 3"]),
                Lineup("Гости", "4-4-2", ["Игрок 11", "Игрок 12", "Игрок 13"])]

    async def get_standings(self, league):
        return [StandingRow(1, "Команда A", 6, 15, 8), StandingRow(2, "Команда C", 6, 12, 4)]


class StubOdds:
    async def get_odds(self, match_id):
        return Odds(match_id, "ТЕСТ", 2.10, 3.30, 3.60, NOW())


class StubMoneyFlow:
    async def get_moneyflow(self, match_id):
        return MoneyFlow(match_id, "ТЕСТ", 55.0, 20.0, 25.0, None, NOW())
