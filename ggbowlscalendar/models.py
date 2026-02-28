"""
Data models for the bowls calendar generator.

Defines the core data structures: Team, Match, and League.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time
from typing import Optional

TBD = "tbd"  # sentinel value in YAML for an unscheduled match date
TBD_DISPLAY = "-date-TBD-"

# Maps YAML venue key → normalised string stored on the match
VENUE_HOME = "home"
VENUE_AWAY = "away"


# ---------------------------------------------------------------------------
# Teams
# ---------------------------------------------------------------------------


@dataclass
class Team:
    """A team and its home location."""

    team_id: str
    name: str
    location: str


class TeamRegistry:
    """Looks up teams by ID, built from the teams YAML file."""

    def __init__(self, teams: dict[str, Team]) -> None:
        self._teams = teams

    @classmethod
    def from_dict(cls, data: dict) -> TeamRegistry:
        """Build a TeamRegistry from the parsed teams.yml dict."""
        teams = {
            team_id: Team(
                team_id=team_id,
                name=td["name"],
                location=td["location"],
            )
            for team_id, td in data.items()
        }
        return cls(teams)

    def get(self, team_id: str) -> Team:
        """
        Return the Team for *team_id*.

        Club-internal competitions are normalised to a single CLUBCOMP entry.
        Unknown teams get a placeholder so the rest of the app can keep running.
        """
        lookup_id = "CLUBCOMP" if team_id.startswith("Club") else team_id
        if lookup_id in self._teams:
            return self._teams[lookup_id]
        # Unknown team — return a placeholder so output still works
        return Team(team_id=team_id, name=f"***{team_id}***", location="TBD")


# ---------------------------------------------------------------------------
# Matches
# ---------------------------------------------------------------------------


@dataclass
class Match:
    """A single scheduled or played league match."""

    venue: str           # VENUE_HOME or VENUE_AWAY
    opp_id: str          # opponent team ID (key into TeamRegistry)
    date: date           # original scheduled date
    start_time: time     # original scheduled time
    our_score: int = 0   # 0-0 means not yet played
    opp_score: int = 0
    rescheduled_date: Optional[date] = None   # overrides date when set
    rescheduled_time: Optional[time] = None   # overrides start_time when set
    sub_team: Optional[str] = None    # e.g. "A", "B" for multi-team clubs
    label: str = ""
    neutral_venue_id: Optional[str] = None   # team ID whose ground is used

    # ------------------------------------------------------------------
    # Derived properties
    # ------------------------------------------------------------------

    @property
    def played(self) -> bool:
        """True if the match has been played.

        Both scores are always present; 0-0 is the unplayed sentinel since a
        genuine 0-0 result is not possible in bowls.
        """
        return not (self.our_score == 0 and self.opp_score == 0)

    @property
    def result(self) -> str:
        """'W', 'L', 'D', or ' ' (not yet played)."""
        if not self.played:
            return " "
        if self.our_score > self.opp_score:
            return "W"
        if self.opp_score > self.our_score:
            return "L"
        return "D"

    @property
    def is_home(self) -> bool:
        return self.venue == VENUE_HOME

    @property
    def effective_date(self) -> Optional[date]:
        """The date on which the match will actually be played."""
        if self.rescheduled_date == TBD:
            return None  # date not yet known
        return self.rescheduled_date or self.date

    @property
    def effective_time(self) -> time:
        """The time at which the match will actually start."""
        return self.rescheduled_time or self.start_time

    def scheduled_datetime(self) -> Optional[datetime]:
        """
        Combined effective date + time, or None if the date is TBD.

        Returns None rather than raising so callers can safely skip
        unscheduled matches.
        """
        eff_date = self.effective_date
        if eff_date is None:
            return None
        return datetime.combine(eff_date, self.effective_time)

    def original_datetime(self) -> datetime:
        """
        The original (pre-reschedule) date+time, used to build stable
        calendar UIDs that survive rescheduling.
        """
        return datetime.combine(self.date, self.start_time)

    def score_display(self) -> tuple[str, str]:
        """Return (our_score_str, opp_score_str), or ('', '') if unplayed."""
        if not self.played:
            return "", ""
        return str(self.our_score), str(self.opp_score)

    def notes(self) -> str:
        """Any label text attached to the match."""
        return self.label


# ---------------------------------------------------------------------------
# League
# ---------------------------------------------------------------------------


@dataclass
class League:
    """All the data for a single team's season in one league."""

    my_team_id: str
    duration_hours: int
    default_day: str   # e.g. "Tue" — used to highlight non-standard match days
    default_time: time  # default kick-off time — used to suppress printing when unchanged
    matches: list[Match] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> League:
        """Build a League from the parsed games YAML dict."""
        my_team_id = data["me"]
        duration = data["duration"]
        default_time = _parse_time(data["start_time"])
        default_day = data["day"]

        matches = [
            _match_from_dict(md, default_time)
            for md in data.get("matches", [])
        ]
        return cls(
            my_team_id=my_team_id,
            duration_hours=duration,
            default_day=default_day,
            default_time=default_time,
            matches=matches,
        )


def _parse_time(value: str | time) -> time:
    """
    Parse a time value from YAML into a datetime.time object.

    YAML may give us the value already as a datetime.time (if written as
    HH:MM:SS) or as a plain string (if written as "HH:MM"). We handle both.
    """
    if isinstance(value, time):
        return value
    return datetime.strptime(value, "%H:%M").time()


def _match_from_dict(data: dict, default_time: time) -> Match:
    """Parse a single match entry from the YAML matches list."""
    if "home" in data:
        venue, opp_id = VENUE_HOME, data["home"]
    else:
        venue, opp_id = VENUE_AWAY, data["away"]

    raw_new_time = data.get("newtime")

    return Match(
        venue=venue,
        opp_id=opp_id,
        date=data["date"],
        start_time=_parse_time(data.get("start_time", default_time)),
        our_score=int(data["our_score"]),
        opp_score=int(data["opp_score"]),
        rescheduled_date=data.get("newdate"),
        rescheduled_time=_parse_time(raw_new_time) if raw_new_time else None,
        sub_team=data.get("team"),
        label=data.get("label", ""),
        neutral_venue_id=data.get("location"),
    )
