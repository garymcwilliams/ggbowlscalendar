"""
Team League Results Management System

This script allows you to manage team league results by reading data from YAML files
containing the results and team details.

Usage:
    python league_results.py --results-file <RESULTS_FILE> --teams-file <TEAMS_FILE>

You can also set the environment variables RESULTS_FILE and TEAMS_FILE
to specify the YAML filenames.

The YAML file containing the results should be formatted as follows:

---
me: team
duration: 3
matches:
  - home: Opponent B
    date: 2023-05-01
    our_score: 3
    opp_score: 2

  - away: Opponent C
    date: 2023-05-01
    our_score: 3
    opp_score: 2

The YAML file containing the team details should be formatted as follows:

---
Opponent B:
  name: Team B
  location: location B

Opponent C:
  name: Team C
  location: location C
"""

import argparse

from envparse import env

from league_results_manager import LeagueResultsManager
from team_manager import TeamManager
from results_table_printer import ResultsTablePrinter


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
