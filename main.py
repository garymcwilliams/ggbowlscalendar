"""
Team League Results Management System

This script allows you to manage team league results by reading data from YAML files
containing the results and team details.

Usage:
    python main.py --team <TEAM_NAME> --year <YEAR>
    
e.g.
    python main.py --team fallsoutdoora --year 2023


You can also set the environment variables ICAL_TEAM and ICAL_YEAR
to specify the parameters.
"""

import argparse

from envparse import env

from ggbowlscalendar.league_results_manager import LeagueResultsManager
from ggbowlscalendar.team_manager import TeamManager
from ggbowlscalendar.results_table_printer import ResultsTablePrinter


def main() -> None:
    """
    Main entry point of the script.
    """
    parser = argparse.ArgumentParser(description="Process Bowls matches.")
    parser.add_argument("-t", "--team")
    parser.add_argument("-y", "--year")

    args = parser.parse_args()

    team = args.team if args.team is not None else env('ICAL_TEAM')
    year = args.year if args.year is not None else env('ICAL_YEAR')

    results_manager = LeagueResultsManager.from_yaml(team, year)
    teams_manager = TeamManager.from_yaml("teams")

    printer = ResultsTablePrinter(results_manager, teams_manager)
    printer.print()


if __name__ == "__main__":
    main()
