"""
iCalendar (.ics) generator for league matches.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

from icalendar import Alarm, Calendar
from icalendar.cal import Event

from .models import League, Match, TeamRegistry

LOGGER = logging.getLogger(__name__)

CALENDAR_DOMAIN = "mc-williams.co.uk"
CALENDAR_PRODID = f"-//Bowling Calendar//{CALENDAR_DOMAIN}//"
CALENDAR_TIMEZONE = "Europe/London"
ALARM_OFFSET = timedelta(hours=-1)
EVENT_PRE_START_BUFFER = timedelta(minutes=10)


def build_calendar(league: League, registry: TeamRegistry) -> Calendar:
    """
    Build and return an iCalendar object for all scheduled matches in *league*.

    Matches with no confirmed date (TBD) are silently skipped.
    """
    if not league.matches:
        LOGGER.warning("No matches found — calendar will be empty.")

    cal = Calendar()
    _add_calendar_headers(cal)

    now = datetime.now(timezone.utc)
    my_team = registry.get(league.my_team_id)

    for match in league.matches:
        match_dt = match.scheduled_datetime()
        if match_dt is None:
            LOGGER.debug("Skipping TBD match vs %s", match.opp_id)
            continue

        event = _build_event(match, match_dt, league, registry, my_team.name, my_team.location, now)
        cal.add_component(event)
        LOGGER.debug("Added event: %s", event.get("summary"))

    return cal


def _add_calendar_headers(cal: Calendar) -> None:
    cal.add("prodid", CALENDAR_PRODID)
    cal.add("version", "2.0")
    cal.add("calscale", "GREGORIAN")
    cal.add("X-WR-TIMEZONE", CALENDAR_TIMEZONE)


def _build_event(
    match: Match,
    match_dt: datetime,
    league: League,
    registry: TeamRegistry,
    my_team_name: str,
    my_team_location: str,
    now: datetime,
) -> Event:
    opp = registry.get(match.opp_id)
    opp_name = _resolve_opp_name(match, opp.name)
    location = _resolve_location(match, registry, my_team_location, opp.location)

    start = match_dt - EVENT_PRE_START_BUFFER
    end = match_dt + timedelta(hours=league.duration_hours)

    event = Event()
    event["uid"] = _calendar_uid(match, league.my_team_id)
    event["location"] = location
    event.add("priority", 5)
    event.add("summary", _build_summary(match, opp_name, my_team_name))
    event.add("description", _build_description(match, opp_name))
    event.add("dtstart", start)
    event.add("dtend", end)
    event.add("dtstamp", now)

    alarm = Alarm()
    alarm.add("action", "DISPLAY")
    alarm.add("description", "Reminder")
    alarm.add("trigger", ALARM_OFFSET)
    event.add_component(alarm)

    return event


def _resolve_opp_name(match: Match, raw_name: str) -> str:
    """Clean up the opponent display name."""
    if raw_name.startswith("***"):
        return raw_name.replace("*", "")
    if raw_name.startswith("Club"):
        return match.opp_id
    return f"{raw_name} {match.sub_team}" if match.sub_team else raw_name


def _resolve_location(
    match: Match,
    registry: TeamRegistry,
    my_team_location: str,
    opp_location: str,
) -> str:
    """Return the address/location string for the event."""
    if match.neutral_venue_id:
        neutral = registry.get(match.neutral_venue_id)
        LOGGER.debug("Neutral venue: %s", neutral.location)
        return neutral.location
    return my_team_location if match.is_home else opp_location


def _build_summary(match: Match, opp_name: str, my_team_name: str) -> str:
    """Return the calendar event title."""
    # Club-internal comp — just use the comp ID
    if opp_name.startswith("Club"):
        return match.opp_id

    home, away = (
        (my_team_name, f"({opp_name})")
        if match.is_home
        else (f"({opp_name})", my_team_name)
    )
    names = f"{home} v {away}"

    if not match.played:
        return f"{names} {match.label}".rstrip()

    our, their = match.score_display()
    return f"{names} {match.result} ({our} - {their}) {match.label}".rstrip()


def _build_description(match: Match, opp_name: str) -> str:
    """Return the calendar event description."""
    venue_label = "neutral" if match.neutral_venue_id else match.venue
    return f"{match.result} {venue_label} ({opp_name})".strip()


def _calendar_uid(match: Match, my_team_id: str) -> str:
    """
    Build a stable unique ID for a match.

    Uses the *original* date/time (not rescheduled) so the UID doesn't
    change when a match is moved.  The label is included to handle the edge
    case of a team playing twice on the same day (#35).
    """
    id_time = match.original_datetime().strftime("%Y%m%d%H%M")
    label = match.label.replace(" ", "") if match.label else ""
    team = my_team_id.replace(" ", "")
    return f"{team}-{id_time}{label}@{CALENDAR_DOMAIN}"
