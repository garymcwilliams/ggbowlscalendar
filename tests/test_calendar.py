"""
Tests for calendar.py — iCalendar generation.
"""

from __future__ import annotations

from datetime import date, datetime, time, timedelta, timezone
from unittest.mock import patch

import pytest

from conftest import (
    FakeAlarm, FakeCalendar, FakeEvent,
    FIXED_NOW, MATCH_DATE, MATCH_TIME,
    make_match, make_league,
)
from ggbowlscalendar.calendar import (
    ALARM_OFFSET,
    CALENDAR_DOMAIN,
    CALENDAR_PRODID,
    CALENDAR_TIMEZONE,
    EVENT_PRE_START_BUFFER,
    _build_description,
    _build_summary,
    _calendar_uid,
    _resolve_location,
    _resolve_opp_name,
    build_calendar,
)
from ggbowlscalendar.models import TBD, VENUE_AWAY, VENUE_HOME


# ---------------------------------------------------------------------------
# Helper — build a calendar with a patched 'now'
# ---------------------------------------------------------------------------

def _build_with_now(matches, registry):
    league = make_league(matches)
    with patch("ggbowlscalendar.calendar.datetime") as mock_dt:
        mock_dt.now.return_value = FIXED_NOW
        mock_dt.combine = datetime.combine
        mock_dt.strptime = datetime.strptime
        return build_calendar(league, registry)


def _events(cal) -> list:
    return [c for c in cal.get("_components", []) if isinstance(c, FakeEvent)]


# ===========================================================================
# _resolve_opp_name
# ===========================================================================

class TestResolveOppName:

    def test_normal_team_returned_unchanged(self):
        assert _resolve_opp_name(make_match(), "Opponents FC") == "Opponents FC"

    def test_stars_stripped_from_unknown_team(self):
        assert _resolve_opp_name(make_match(), "***UNKNOWN***") == "UNKNOWN"

    def test_club_comp_returns_opp_id(self):
        m = make_match(opp_id="ClubKnockout")
        assert _resolve_opp_name(m, "Club Championship") == "ClubKnockout"

    def test_sub_team_appended(self):
        m = make_match(sub_team="A")
        assert _resolve_opp_name(m, "Opponents FC") == "Opponents FC A"

    def test_no_sub_team_suffix_when_none(self):
        assert _resolve_opp_name(make_match(), "Opponents FC") == "Opponents FC"


# ===========================================================================
# _resolve_location
# ===========================================================================

class TestResolveLocation:

    def test_home_match_uses_my_location(self, registry):
        m = make_match(venue=VENUE_HOME)
        assert _resolve_location(m, registry, "My Ground, Town", "Their Ground, City") == "My Ground, Town"

    def test_away_match_uses_opp_location(self, registry):
        m = make_match(venue=VENUE_AWAY)
        assert _resolve_location(m, registry, "My Ground, Town", "Their Ground, City") == "Their Ground, City"

    def test_neutral_venue_overrides_both(self, registry):
        m = make_match(neutral_venue_id="NEUTRAL")
        assert _resolve_location(m, registry, "My Ground, Town", "Their Ground, City") == "Neutral Ground, Village"


# ===========================================================================
# _build_summary
# ===========================================================================

class TestBuildSummary:

    @pytest.mark.parametrize("venue, expected", [
        (VENUE_HOME, "My Bowls Club v (Opponents FC)"),
        (VENUE_AWAY, "(Opponents FC) v My Bowls Club"),
    ])
    def test_unplayed_format(self, venue, expected):
        m = make_match(venue=venue)
        assert _build_summary(m, "Opponents FC", "My Bowls Club") == expected

    @pytest.mark.parametrize("venue, our, their, result_code, expected", [
        (VENUE_HOME, 5, 2, "W", "My Bowls Club v (Opponents FC) W (5 - 2)"),
        (VENUE_AWAY, 1, 4, "L", "(Opponents FC) v My Bowls Club L (1 - 4)"),
        (VENUE_HOME, 3, 3, "D", "My Bowls Club v (Opponents FC) D (3 - 3)"),
    ])
    def test_played_format(self, venue, our, their, result_code, expected):
        m = make_match(venue=venue, our_score=our, opp_score=their)
        assert _build_summary(m, "Opponents FC", "My Bowls Club") == expected

    def test_label_included_when_unplayed(self):
        m = make_match(label="Cup Semi")
        assert "Cup Semi" in _build_summary(m, "Opponents FC", "My Bowls Club")

    def test_label_included_when_played(self):
        m = make_match(our_score=2, opp_score=1, label="Final")
        assert "Final" in _build_summary(m, "Opponents FC", "My Bowls Club")

    def test_no_trailing_whitespace_without_label(self):
        s = _build_summary(make_match(), "Opponents FC", "My Bowls Club")
        assert s == s.rstrip()

    def test_club_comp_returns_opp_id(self):
        m = make_match(opp_id="ClubKnockout")
        assert _build_summary(m, "ClubKnockout", "My Bowls Club") == "ClubKnockout"


# ===========================================================================
# _build_description
# ===========================================================================

class TestBuildDescription:

    @pytest.mark.parametrize("venue, our, their, expected", [
        (VENUE_HOME, 0, 0, "home (Opponents FC)"),
        (VENUE_AWAY, 3, 1, "W away (Opponents FC)"),
    ])
    def test_description_format(self, venue, our, their, expected):
        m = make_match(venue=venue, our_score=our, opp_score=their)
        assert _build_description(m, "Opponents FC") == expected

    def test_neutral_venue_label(self):
        m = make_match(neutral_venue_id="NEUTRAL", our_score=2, opp_score=2)
        assert _build_description(m, "Opponents FC") == "D neutral (Opponents FC)"

    def test_no_leading_or_trailing_whitespace(self):
        d = _build_description(make_match(), "Opponents FC")
        assert d == d.strip()


# ===========================================================================
# _calendar_uid
# ===========================================================================

class TestCalendarUid:

    def test_format(self):
        m = make_match(match_date=date(2024, 5, 14), start_time=time(18, 0))
        assert _calendar_uid(m, "MYTEAM") == f"MYTEAM-202405141800@{CALENDAR_DOMAIN}"

    def test_uses_original_date_not_rescheduled(self):
        m = make_match(
            match_date=date(2024, 5, 14), start_time=time(18, 0),
            rescheduled_date=date(2024, 6, 1), rescheduled_time=time(10, 0),
        )
        uid = _calendar_uid(m, "MYTEAM")
        assert "202405141800" in uid
        assert "202406011000" not in uid

    def test_label_included_without_spaces(self):
        m = make_match(match_date=date(2024, 5, 14), start_time=time(18, 0), label="Cup Final")
        assert "CupFinal" in _calendar_uid(m, "MYTEAM")

    def test_spaces_stripped_from_team_id(self):
        m = make_match(match_date=date(2024, 5, 14), start_time=time(18, 0))
        uid = _calendar_uid(m, "MY TEAM")
        assert "MYTEAM-" in uid
        assert " " not in uid

    def test_ends_with_domain(self):
        m = make_match(match_date=date(2024, 5, 14), start_time=time(18, 0))
        assert _calendar_uid(m, "MYTEAM").endswith(f"@{CALENDAR_DOMAIN}")


# ===========================================================================
# build_calendar — calendar headers
# ===========================================================================

class TestCalendarHeaders:

    def test_prodid(self, registry):
        cal = _build_with_now([], registry)
        assert cal["prodid"] == CALENDAR_PRODID

    def test_version(self, registry):
        cal = _build_with_now([], registry)
        assert cal["version"] == "2.0"

    def test_calscale(self, registry):
        cal = _build_with_now([], registry)
        assert cal["calscale"] == "GREGORIAN"

    def test_timezone(self, registry):
        cal = _build_with_now([], registry)
        assert cal["X-WR-TIMEZONE"] == CALENDAR_TIMEZONE


# ===========================================================================
# build_calendar — event counts
# ===========================================================================

class TestBuildCalendarEventCounts:

    def test_empty_league_produces_no_events(self, registry):
        assert _events(_build_with_now([], registry)) == []

    def test_tbd_match_excluded(self, registry):
        m = make_match(rescheduled_date=TBD)
        assert _events(_build_with_now([m], registry)) == []

    def test_scheduled_match_produces_one_event(self, registry):
        assert len(_events(_build_with_now([make_match()], registry))) == 1

    def test_multiple_matches_produce_multiple_events(self, registry):
        matches = [
            make_match(match_date=date(2024, 5, 14)),
            make_match(match_date=date(2024, 5, 21), venue=VENUE_AWAY),
        ]
        assert len(_events(_build_with_now(matches, registry))) == 2


# ===========================================================================
# build_calendar — event field values
# ===========================================================================

class TestBuildCalendarEventFields:

    @pytest.fixture
    def event(self, registry):
        cal = _build_with_now([make_match()], registry)
        return _events(cal)[0]

    def test_dtstart_is_10_mins_before_match(self, event):
        assert event["dtstart"] == datetime(2024, 5, 14, 17, 50)

    def test_dtend_is_match_start_plus_duration(self, event):
        assert event["dtend"] == datetime(2024, 5, 14, 21, 0)

    def test_uid_is_stable(self, event):
        assert event["uid"] == f"MYTEAM-202405141800@{CALENDAR_DOMAIN}"

    def test_priority(self, event):
        assert event["priority"] == 5

    def test_dtstamp_uses_now(self, event):
        assert event["dtstamp"] == FIXED_NOW

    @pytest.mark.parametrize("venue, expected_location", [
        (VENUE_HOME, "My Ground, Town"),
        (VENUE_AWAY, "Their Ground, City"),
    ])
    def test_location(self, registry, venue, expected_location):
        cal = _build_with_now([make_match(venue=venue)], registry)
        assert _events(cal)[0]["location"] == expected_location

    def test_location_neutral(self, registry):
        cal = _build_with_now([make_match(neutral_venue_id="NEUTRAL")], registry)
        assert _events(cal)[0]["location"] == "Neutral Ground, Village"

    @pytest.mark.parametrize("venue, expected_summary", [
        (VENUE_HOME, "My Bowls Club v (Opponents FC)"),
        (VENUE_AWAY, "(Opponents FC) v My Bowls Club"),
    ])
    def test_summary_unplayed(self, registry, venue, expected_summary):
        cal = _build_with_now([make_match(venue=venue)], registry)
        assert _events(cal)[0]["summary"] == expected_summary

    def test_summary_played_away_win(self, registry):
        m = make_match(venue=VENUE_AWAY, our_score=5, opp_score=1)
        cal = _build_with_now([m], registry)
        assert _events(cal)[0]["summary"] == "(Opponents FC) v My Bowls Club W (5 - 1)"


# ===========================================================================
# build_calendar — alarm
# ===========================================================================

class TestBuildCalendarAlarm:

    @pytest.fixture
    def alarm(self, registry):
        cal = _build_with_now([make_match()], registry)
        event = _events(cal)[0]
        alarms = [c for c in event.get("_components", []) if isinstance(c, FakeAlarm)]
        assert len(alarms) == 1
        return alarms[0]

    def test_alarm_action(self, alarm):
        assert alarm["action"] == "DISPLAY"

    def test_alarm_trigger(self, alarm):
        assert alarm["trigger"] == timedelta(hours=-1)

    def test_alarm_description(self, alarm):
        assert alarm["description"] == "Reminder"
