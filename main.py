"""
Team League Results Management System

This script allows you to manage team league results by reading data from YAML
files
containing the results and team details.

Usage:
    python main.py --team <TEAM_NAME> --year <YEAR>

e.g.
    python main.py --team fallsoutdoora --year 2023


You can also set the environment variables ICAL_TEAM and ICAL_YEAR
to specify the parameters.
"""

import argparse
import logging
import logging.config
import os

import yaml
from envparse import env

from ggbowlscalendar.league_results_manager import LeagueResultsManager
from ggbowlscalendar.results_table_ical import ResultsTableIcal
from ggbowlscalendar.results_table_printer import ResultsTablePrinter
from ggbowlscalendar.team_manager import TeamManager
from ggbowlscalendar.utils import get_games_data, get_teams_data, write_ical_file


def setup_logging(
    default_path="logging.yml",
    default_level=logging.INFO,
):
    """Setup logging configuration"""
    path = default_path
    if os.path.exists(path):
        with open(path, "rt", encoding="utf-8") as config:
            config = yaml.safe_load(config.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def main() -> None:
    """
    Main entry point of the script.
    """
    setup_logging()

    logger = logging.getLogger("__main__")
    logger.debug("================================ Running")

    parser = argparse.ArgumentParser(description="Process Bowls matches.")
    parser.add_argument("-t", "--team")
    parser.add_argument("-y", "--year")

    args = parser.parse_args()

    team = args.team if args.team is not None else env("ICAL_TEAM")
    year = args.year if args.year is not None else env("ICAL_YEAR")
    logger.debug("using %s %s", team, year)

    games_data = get_games_data(team, year)
    results_manager = LeagueResultsManager.from_dict(games_data)

    teams_data = get_teams_data()
    teams_manager = TeamManager.from_dict(teams_data)

    logger.debug("Printing")
    printer = ResultsTablePrinter(results_manager, teams_manager)
    printer.print()

    logger.debug("Generating ical")
    ical_generator = ResultsTableIcal(results_manager, teams_manager)
    ical_generator.generate_ical()
    filename = f"{team}_{year}-51.ics"
    write_ical_file(filename, ical_generator.cal.to_ical())


if __name__ == "__main__":
    main()
