"""
Tests for models.py — _parse_time, Team, TeamRegistry, Match, League.
"""

from __future__ import annotations

from datetime import date, datetime, time

import pytest

from conftest import make_match, make_league, MATCH_DATE, MATCH_TIME
from ggbowlscalendar.models import (
    TBD,
    TBD_DISPLAY,
    VENUE_AWAY,
    VENUE_HOME,
    League,
    Match,
    Team,
    TeamRegistry,
    _match_from_dict,
    _parse_time,
)


# ===========================================================================
# _parse_time
# ===========================================================================

class TestParseTime:

    def test_parses_hhmm_string(self):
        assert _parse_time("18:30") == time(18, 30)

    def test_passes_through_existing_time_object(self):
        t = time(9, 15)
        assert _parse_time(t) is t

    def test_parses_midnight(self):
        assert _parse_time("00:00") == time(0, 0)

    def test_invalid_string_raises_value_error(self):
        with pytest.raises(ValueError):
            _parse_time("25:00")


# ===========================================================================
# Team
# ===========================================================================

class TestTeam:

    def test_stores_all_fields(self):
        team = Team(team_id="T1", name="Test Team", location="Test Ground")
        assert team.team_id == "T1"
        assert team.name == "Test Team"
        assert team.location == "Test Ground"


# ===========================================================================
# TeamRegistry
# ===========================================================================

class TestTeamRegistry:

    def test_get_known_team(self, registry):
        team = registry.get("OPP1")
        assert team.name == "Opponents FC"
        assert team.location == "Their Ground, City"

    def test_unknown_team_returns_placeholder_name(self, registry):
        assert registry.get("UNKNOWN").name == "***UNKNOWN***"

    def test_unknown_team_returns_tbd_location(self, registry):
        assert registry.get("UNKNOWN").location == "TBD"

    def test_unknown_team_preserves_original_id(self, registry):
        assert registry.get("UNKNOWN").team_id == "UNKNOWN"

    def test_club_prefix_resolves_to_clubcomp(self, registry):
        assert registry.get("ClubChampionship").name == "Club Championship"

    def test_from_dict_creates_all_teams(self):
        data = {
            "A": {"name": "Team A", "location": "Loc A"},
            "B": {"name": "Team B", "location": "Loc B"},
        }
        reg = TeamRegistry.from_dict(data)
        assert reg.get("A").name == "Team A"
        assert reg.get("B").name == "Team B"


# ===========================================================================
# Match — is_home / notes
# ===========================================================================

class TestMatchProperties:

    def test_is_home_true(self, home_match):
        assert home_match.is_home is True

    def test_is_home_false_when_away(self, away_match):
        assert away_match.is_home is False

    def test_notes_returns_label(self):
        assert make_match(label="Cup Final").notes() == "Cup Final"

    def test_notes_empty_by_default(self, home_match):
        assert home_match.notes() == ""


# ===========================================================================
# Match — played / result
# ===========================================================================

class TestMatchResult:

    def test_not_played_when_scores_are_none(self):
        m = make_match(our_score=None, opp_score=None)
        assert m.played is False
        assert m.result == " "

    def test_played_when_both_scores_present(self, played_win):
        assert played_win.played is True

    def test_win(self, played_win):
        assert played_win.result == "W"

    def test_loss(self, played_loss):
        assert played_loss.result == "L"

    def test_draw(self, played_draw):
        assert played_draw.result == "D"

    def test_zero_zero_is_unplayed(self):
        """0-0 is the unplayed sentinel — a genuine 0-0 result is impossible in bowls."""
        m = make_match(our_score=0, opp_score=0)
        assert m.played is False
        assert m.result == " "

    @pytest.mark.parametrize("our, their, expected", [
        (5, 2, "W"),
        (1, 4, "L"),
        (3, 3, "D"),
    ])
    def test_result_codes(self, our, their, expected):
        assert make_match(our_score=our, opp_score=their).result == expected


# ===========================================================================
# Match — score_display
# ===========================================================================

class TestScoreDisplay:

    def test_unplayed_returns_none_pair(self):
        assert make_match().score_display() == (None, None)

    def test_played_returns_string_pair(self, played_win):
        assert played_win.score_display() == ("5", "2")

    def test_zero_zero_returns_none_pair(self):
        """0-0 means unplayed, so score_display returns (None, None)."""
        assert make_match(our_score=0, opp_score=0).score_display() == (None, None)


# ===========================================================================
# Match — scheduling
# ===========================================================================

class TestMatchScheduling:

    def test_effective_date_uses_original_when_no_reschedule(self):
        assert make_match(match_date=date(2024, 6, 1)).effective_date == date(2024, 6, 1)

    def test_effective_date_uses_rescheduled_date(self):
        m = make_match(match_date=date(2024, 6, 1), rescheduled_date=date(2024, 6, 15))
        assert m.effective_date == date(2024, 6, 15)

    def test_effective_date_is_none_when_tbd(self):
        assert make_match(rescheduled_date=TBD).effective_date is None

    def test_effective_time_uses_original(self):
        assert make_match(start_time=time(18, 0)).effective_time == time(18, 0)

    def test_effective_time_uses_rescheduled(self):
        m = make_match(start_time=time(18, 0), rescheduled_time=time(14, 30))
        assert m.effective_time == time(14, 30)

    def test_scheduled_datetime_normal(self):
        m = make_match(match_date=date(2024, 5, 14), start_time=time(18, 0))
        assert m.scheduled_datetime() == datetime(2024, 5, 14, 18, 0)

    def test_scheduled_datetime_uses_reschedule(self):
        m = make_match(
            match_date=date(2024, 5, 14), start_time=time(18, 0),
            rescheduled_date=date(2024, 5, 21), rescheduled_time=time(14, 0),
        )
        assert m.scheduled_datetime() == datetime(2024, 5, 21, 14, 0)

    def test_scheduled_datetime_returns_none_for_tbd(self):
        assert make_match(rescheduled_date=TBD).scheduled_datetime() is None

    def test_original_datetime_ignores_reschedule(self):
        """UID stability: original_datetime must not change when a match is moved."""
        m = make_match(
            match_date=date(2024, 5, 14), start_time=time(18, 0),
            rescheduled_date=date(2024, 5, 28), rescheduled_time=time(10, 0),
        )
        assert m.original_datetime() == datetime(2024, 5, 14, 18, 0)


# ===========================================================================
# _match_from_dict
# ===========================================================================

BASE_DICT = {"home": "OPP1", "date": date(2024, 5, 14)}
DEFAULT_TIME = time(18, 0)


class TestMatchFromDict:

    def _parse(self, data: dict) -> Match:
        return _match_from_dict(data, DEFAULT_TIME)

    def test_home_venue(self):
        m = self._parse(BASE_DICT)
        assert m.venue == VENUE_HOME
        assert m.opp_id == "OPP1"

    def test_away_venue(self):
        m = self._parse({"away": "OPP2", "date": date(2024, 6, 1)})
        assert m.venue == VENUE_AWAY
        assert m.opp_id == "OPP2"

    def test_uses_default_time_when_not_specified(self):
        assert self._parse(BASE_DICT).start_time == DEFAULT_TIME

    def test_per_match_start_time_overrides_default(self):
        assert self._parse({**BASE_DICT, "start_time": "10:00"}).start_time == time(10, 0)

    def test_scores_parsed_as_ints(self):
        m = self._parse({**BASE_DICT, "our_score": 5, "opp_score": 3})
        assert isinstance(m.our_score, int)
        assert isinstance(m.opp_score, int)
        assert (m.our_score, m.opp_score) == (5, 3)

    def test_missing_scores_default_to_none(self):
        m = self._parse(BASE_DICT)
        assert m.our_score is None
        assert m.opp_score is None

    def test_zero_scores_stored_as_none(self):
        """Explicit 0-0 in YAML means unplayed, stored as None."""
        m = self._parse({**BASE_DICT, "our_score": 0, "opp_score": 0})
        assert m.our_score is None
        assert m.opp_score is None

    def test_newdate_and_newtime_parsed(self):
        m = self._parse({**BASE_DICT, "newdate": date(2024, 6, 1), "newtime": "14:30"})
        assert m.rescheduled_date == date(2024, 6, 1)
        assert m.rescheduled_time == time(14, 30)

    def test_tbd_newdate_preserved(self):
        assert self._parse({**BASE_DICT, "newdate": TBD}).rescheduled_date == TBD

    def test_label_defaults_to_empty_string(self):
        assert self._parse(BASE_DICT).label == ""

    def test_label_parsed(self):
        assert self._parse({**BASE_DICT, "label": "Cup Final"}).label == "Cup Final"

    def test_sub_team_parsed(self):
        assert self._parse({**BASE_DICT, "team": "A"}).sub_team == "A"

    def test_neutral_venue_parsed(self):
        assert self._parse({**BASE_DICT, "location": "NEUTRAL"}).neutral_venue_id == "NEUTRAL"


# ===========================================================================
# League.from_dict
# ===========================================================================

LEAGUE_DICT = {
    "me": "MYTEAM",
    "duration": 3,
    "start_time": "18:00",
    "day": "Tue",
    "matches": [
        {"home": "OPP1", "date": date(2024, 5, 14)},
        {"away": "OPP2", "date": date(2024, 5, 21), "our_score": 4, "opp_score": 2},
    ],
}


class TestLeagueFromDict:

    def test_my_team_id(self):
        assert League.from_dict(LEAGUE_DICT).my_team_id == "MYTEAM"

    def test_duration_hours(self):
        assert League.from_dict(LEAGUE_DICT).duration_hours == 3

    def test_default_day(self):
        assert League.from_dict(LEAGUE_DICT).default_day == "Tue"

    def test_match_count(self):
        assert len(League.from_dict(LEAGUE_DICT).matches) == 2

    def test_default_time_stored_on_league(self):
        assert League.from_dict(LEAGUE_DICT).default_time == time(18, 0)

    def test_default_time_propagated_to_matches(self):
        assert League.from_dict(LEAGUE_DICT).matches[0].start_time == time(18, 0)

    def test_empty_matches_list(self):
        assert League.from_dict({**LEAGUE_DICT, "matches": []}).matches == []

    def test_played_match_result(self):
        second = League.from_dict(LEAGUE_DICT).matches[1]
        assert second.played is True
        assert second.result == "W"
