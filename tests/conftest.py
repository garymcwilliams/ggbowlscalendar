"""
conftest.py — shared fixtures and module stubs for the ggbowlscalendar test suite.

The stubs for icalendar, rich, and envparse are registered here so they are
available before any ggbowlscalendar module is imported, regardless of the
order pytest collects the test files.
"""

from __future__ import annotations

import sys
import types
from datetime import date, datetime, time, timezone

import pytest

from ggbowlscalendar.models import League, Match, TeamRegistry, VENUE_AWAY, VENUE_HOME


# ---------------------------------------------------------------------------
# Module stubs
# (registered at collection time so imports in test files always succeed)
# ---------------------------------------------------------------------------

class _FakeTable:
    def __init__(self, **kwargs):
        self.columns: list[str] = []
        self.rows: list[tuple] = []

    def add_column(self, name: str) -> None:
        self.columns.append(name)

    def add_row(self, *args) -> None:
        self.rows.append(args)


class _FakeConsole:
    def __init__(self):
        self.printed: list = []

    def print(self, *args, **kwargs) -> None:
        self.printed.extend(args)


class _ICalComponent(dict):
    """Minimal iCalendar component — stores properties as a plain dict."""

    def add(self, key: str, value) -> None:
        self[key] = value

    def add_component(self, comp) -> None:
        self.setdefault("_components", []).append(comp)


class FakeCalendar(_ICalComponent):
    pass


class FakeEvent(_ICalComponent):
    pass


class FakeAlarm(_ICalComponent):
    pass


def _register_stubs() -> None:
    stubs: list[tuple[str, dict]] = [
        ("rich",          {}),
        ("rich.console",  {"Console": _FakeConsole}),
        ("rich.table",    {"Table": _FakeTable}),
        ("icalendar",     {"Calendar": FakeCalendar, "Alarm": FakeAlarm}),
        ("icalendar.cal", {"Event": FakeEvent}),
        ("envparse",      {
            "env": types.SimpleNamespace(read_envfile=lambda: None, str=lambda k: "")
        }),
    ]
    for mod_name, attrs in stubs:
        mod = sys.modules.get(mod_name) or types.ModuleType(mod_name)
        for k, v in attrs.items():
            setattr(mod, k, v)
        sys.modules[mod_name] = mod


_register_stubs()


# ---------------------------------------------------------------------------
# Shared constants
# ---------------------------------------------------------------------------

FIXED_NOW = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

MATCH_DATE = date(2024, 5, 14)   # a Tuesday
MATCH_TIME = time(18, 0)


# ---------------------------------------------------------------------------
# Factory helpers (used directly in tests or inside fixtures)
# ---------------------------------------------------------------------------

def make_match(
    venue: str = VENUE_HOME,
    opp_id: str = "OPP1",
    match_date: date = MATCH_DATE,
    start_time: time = MATCH_TIME,
    our_score: int | None = None,
    opp_score: int | None = None,
    rescheduled_date=None,
    rescheduled_time: time | None = None,
    sub_team: str | None = None,
    label: str = "",
    neutral_venue_id: str | None = None,
) -> Match:
    return Match(
        venue=venue,
        opp_id=opp_id,
        date=match_date,
        start_time=start_time,
        our_score=our_score,
        opp_score=opp_score,
        rescheduled_date=rescheduled_date,
        rescheduled_time=rescheduled_time,
        sub_team=sub_team,
        label=label,
        neutral_venue_id=neutral_venue_id,
    )


def make_league(matches: list[Match] | None = None) -> League:
    return League(
        my_team_id="MYTEAM",
        duration_hours=3,
        default_day="Tue",
        default_time=MATCH_TIME,
        matches=matches or [],
    )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def registry() -> TeamRegistry:
    return TeamRegistry.from_dict({
        "MYTEAM":   {"name": "My Bowls Club",    "location": "My Ground, Town"},
        "OPP1":     {"name": "Opponents FC",      "location": "Their Ground, City"},
        "NEUTRAL":  {"name": "Neutral Club",      "location": "Neutral Ground, Village"},
        "CLUBCOMP": {"name": "Club Championship", "location": "My Ground, Town"},
    })


@pytest.fixture
def league() -> League:
    return make_league()


@pytest.fixture
def home_match() -> Match:
    return make_match(venue=VENUE_HOME)


@pytest.fixture
def away_match() -> Match:
    return make_match(venue=VENUE_AWAY)


@pytest.fixture
def played_win() -> Match:
    return make_match(our_score=5, opp_score=2)


@pytest.fixture
def played_loss() -> Match:
    return make_match(our_score=1, opp_score=4)


@pytest.fixture
def played_draw() -> Match:
    return make_match(our_score=3, opp_score=3)


@pytest.fixture
def fake_console() -> _FakeConsole:
    return _FakeConsole()


@pytest.fixture
def fake_table() -> _FakeTable:
    return _FakeTable()
