"""
Bowls Calendar Generator

Usage:
    python main.py --team <team-name> --year <year>

Arguments can also be supplied via environment variables:
    ICAL_TEAM   equivalent to --team
    ICAL_YEAR   equivalent to --year

Example:
    python main.py --team fallsindoor --year 2024
    ICAL_TEAM=fallsindoor ICAL_YEAR=2024 python main.py
"""

import argparse
import logging
import logging.config
import os
import sys
from pathlib import Path

import yaml

from ggbowlscalendar.calendar import build_calendar
from ggbowlscalendar.models import League, TeamRegistry
from ggbowlscalendar.printer import print_results
from ggbowlscalendar.utils import load_games_data, load_teams_data, write_ical_file


def _setup_logging() -> None:
    """Configure logging from logging.yml if present, otherwise use a sensible default."""
    config_path = Path("logging.yml")
    if config_path.exists():
        with open(config_path, encoding="utf-8") as fh:
            logging.config.dictConfig(yaml.safe_load(fh))
    else:
        logging.basicConfig(
            level=logging.INFO,
            format="%(levelname)s %(name)s: %(message)s",
        )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a bowls club iCalendar (.ics) file from match data.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Each argument can also be set via an environment variable:\n"
            "  --team  →  ICAL_TEAM\n"
            "  --year  →  ICAL_YEAR\n"
        ),
    )
    parser.add_argument(
        "--team",
        default=os.getenv("ICAL_TEAM"),
        metavar="TEAM_NAME",
        help="Team name used to locate the games YAML file (e.g. 'fallsindoor'). "
             "Falls back to $ICAL_TEAM if not supplied.",
    )
    parser.add_argument(
        "--year",
        default=os.getenv("ICAL_YEAR"),
        metavar="YEAR",
        help="Season year (e.g. '2024'). Falls back to $ICAL_YEAR if not supplied.",
    )

    args = parser.parse_args()

    missing = [
        flag
        for flag, value in (("--team (or $ICAL_TEAM)", args.team),
                             ("--year (or $ICAL_YEAR)", args.year))
        if not value
    ]
    if missing:
        parser.error("the following arguments are required: " + ", ".join(missing))

    return args


def main() -> None:
    _setup_logging()
    logger = logging.getLogger(__name__)

    args = _parse_args()
    team = args.team
    year = args.year

    logger.info("Generating calendar for team=%s year=%s", team, year)

    # Load data
    teams_data = load_teams_data()
    games_data = load_games_data(club=team, year=year)

    # Build models
    registry = TeamRegistry.from_dict(teams_data)
    league = League.from_dict(games_data)

    # Print results table to console
    print_results(league, registry)

    # Generate and save the .ics file
    calendar = build_calendar(league, registry)
    ics_filename = f"{team}_games_{year}.ics"
    write_ical_file(ics_filename, calendar.to_ical())

    logger.info("Done — written %s", ics_filename)


if __name__ == "__main__":
    main()