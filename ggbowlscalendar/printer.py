"""
Console table display for league results.
"""

from __future__ import annotations

import logging
from datetime import datetime as dt, time

from rich.console import Console
from rich.table import Table

from .models import League, Match, TBD_DISPLAY, TeamRegistry

LOGGER = logging.getLogger(__name__)

# Rich markup for each result code
_RESULT_DISPLAY = {
    "W": "[green]W :heavy_check_mark:[/]",
    "L": "[red]L[/]",
    "D": "D",
    " ": " ",
}

_VENUE_COLOUR = {
    "home": "red",
    "away": "blue",
}


def print_results(league: League, registry: TeamRegistry) -> None:
    """Print all matches in *league* as a formatted Rich table."""
    console = Console()

    if not league.matches:
        console.print("No results found.")
        return

    table = _build_table(league, registry)
    console.print(table)


def _build_table(league: League, registry: TeamRegistry) -> Table:
    table = Table(show_header=True, header_style="bold magenta")
    date_hdr_time = league.default_time.strftime("%H-%M")
    for col in ("R", "Venue", "Us", "Opp", "Opponent", f"Date       {date_hdr_time}", "Note"):
        table.add_column(col)

    for match in league.matches:
        table.add_row(*_row_values(match, league, registry))

    return table


def _row_values(
    match: Match, league: League, registry: TeamRegistry
) -> tuple[str, ...]:
    opp = registry.get(match.opp_id)
    opp_name = _display_opp_name(match, opp.name)

    our, their = match.score_display()
    venue_markup = f"[{_VENUE_COLOUR[match.venue]}]{match.venue}[/]"

    return (
        _RESULT_DISPLAY[match.result],
        venue_markup,
        our or "",
        their or "",
        opp_name,
        _format_date(match, league.default_day, league.default_time),
        match.notes(),
    )


def _display_opp_name(match: Match, raw_name: str) -> str:
    """Resolve the display name for the opponent."""
    if raw_name.startswith("***"):
        # Unknown team — highlight in red and show original ID
        name = f"[red]{raw_name}[/red]"
    elif raw_name.startswith("Club"):
        # Internal club competition — use the raw opp_id as the label
        name = match.opp_id
    else:
        name = raw_name

    if match.sub_team:
        name = f"{name} {match.sub_team}"
    return name


def _format_date(match: Match, default_day: str, default_time: time) -> str:
    """Return a formatted date string, or TBD_DISPLAY if not yet scheduled.

    The weekday is suppressed when it matches the league's usual match day.
    The time is suppressed when it matches the league's default kick-off time.
    """
    match_dt = match.scheduled_datetime()
    if match_dt is None:
        return TBD_DISPLAY

    # Only show the weekday when it differs from the team's usual match day
    day_prefix = (
        match_dt.strftime("%a") if match_dt.strftime("%a") != default_day else "   "
    )
    # Only show the time when it differs from the league's default kick-off time
    time_suffix = (
        match_dt.strftime(" %H:%M") if match.effective_time != default_time else ""
    )
    return match_dt.strftime(f"{day_prefix} %d-%b") + time_suffix
