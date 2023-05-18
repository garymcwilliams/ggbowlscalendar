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

import datetime
from typing import List
import argparse

import yaml
from envparse import env

from rich.console import Console
from rich.table import Table


class LeagueResult:
    """Represents a single league result."""

    def __init__(
        self,
        venue: str,
        opp_id: str,
        date: datetime,
        time: str,
        our_score: int,
        opp_score: int,
        newdate: str = None,
        label: str = None,
    ):
        """
        Initialize a LeagueResult instance.

        Args:
            venue (str): The venue associated with the result.
            opp_id (str): The ID of the opponent team.
            date (datetime): The original date of the match.
            time (str): The original time of the match.
            our_score (int): The score of our team.
            opp_score (int): The score of the opponent team.
            newdate (str, optional): The new date of the match (if available).
        """
        self.venue = venue
        self.opp_id = opp_id
        self.date = date
        self.time = time
        self.our_score = float(our_score)
        self.opp_score = float(opp_score)
        self.newdate = newdate
        self.label = label

        self.result = (
            "-" if self.our_score == 0.0 and self.opp_score == 0.0 else
            "W" if our_score > opp_score else
            "L" if our_score < opp_score else
            "D"
        )

    def match_date(self) -> datetime:
        """
        return the match date, allowing newdate to overide the default if
        that has been provided.
        """
        match_date = self.newdate if self.newdate else self.date
        match_time = datetime.datetime.strptime(self.time, '%H:%M').time()
        match_date_time = datetime.datetime.combine(match_date, match_time)

        return match_date_time

    def notes(self) -> str:
        """ return any special notes for printing """
        notes = self.label
        return notes


class LeagueResultsManager:
    """Manages a team league results."""

    def __init__(self, myTeam: str, duration: int, results: List[LeagueResult]) -> None:
        self.myTeam = myTeam
        self.duration = duration
        """
        Initialize a LeagueResultsManager instance.

        Args:
            results (List[LeagueResult]): The list of league results.
        """

        self.results = results

    @classmethod
    def from_yaml(cls, filename: str) -> "LeagueResultsManager":
        """
        Create a LeagueResultsManager instance from a YAML file.

        Args:
            filename (str): The filename of the YAML file.

        Returns:
            LeagueResultsManager: The created LeagueResultsManager instance.
        """
        with open(filename, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        me = data.get("me")
        duration = data.get("duration")
        default_time = data.get("start_time")

        matches_data = data.get("matches", [])
        matches = []
        for result_data in matches_data:
            if "home" in result_data:
                venue = "home"
                opp_id = result_data["home"]
            elif "away" in result_data:
                venue = "away"
                opp_id = result_data["away"]
            else:
                continue

            date = result_data.get("date")
            newdate = result_data.get("newdate")
            our_score = result_data.get("our_score", 0)
            opp_score = result_data.get("opp_score", 0)
            label = result_data.get("label", "")

            result = LeagueResult(venue, opp_id, date, default_time, our_score,
                                  opp_score, newdate, label)
            matches.append(result)

        return cls(me, duration, matches)


class Team:
    """Represents a team."""

    def __init__(self, id: str, name: str, location: str) -> None:
        """
        Initialize a Team instance.

        Args:
            id (str): The ID of the team.
            name (str): The name of the team.
            location (str): The location of the team.
        """
        self.id = id
        self.name = name
        self.location = location


class TeamManager:
    """Manages the team details."""

    def __init__(self, teams: List[Team]) -> None:
        """
        Initialize a TeamManager instance.

        Args:
            teams (List[Team]): The list of teams.
        """
        self.teams = teams

    @classmethod
    def from_yaml(cls, filename: str) -> "TeamManager":
        """
        Create a TeamManager instance from a YAML file.

        Args:
            filename (str): The filename of the YAML file.

        Returns:
            TeamManager: The created TeamManager instance.
        """
        with open(filename, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        teams = []
        for team_id, team_data in data.items():
            team = Team(id=team_id, name=team_data["name"],
                        location=team_data["location"])
            teams.append(team)

        return cls(teams)

    def get_team_details(self, team_id: str) -> dict:
        """
        Get the details of a team.

        Args:
            team_id (str): The ID of the team.

        Returns:
            dict: The team details.
        """
        team = next((team for team in self.teams if team.id == team_id), None)
        if team:
            return {"name": team.name, "location": team.location}
        return {}


class ResultsTablePrinter:
    """Print results in a Table"""

    def __init__(self, results_manager: LeagueResultsManager,
                 team_manager: TeamManager) -> None:
        self.results_manager = results_manager
        self.team_manager = team_manager
        self.console = Console()
        self.table = Table(show_header=True, header_style="bold magenta")

    def print(self) -> None:
        """
        Display the league results.

        Args:
            results_manager (LeagueResultsManager): The manager containing the
            results.
            team_manager (TeamManager): The team manager containing the team
            details.
        """

        self._print_table_header()

        for result in self.results_manager.results:
            my_team_details = self.team_manager.get_team_details(
                self.results_manager.myTeam)
            opp_team_details = self.team_manager.get_team_details(
                result.opp_id)

            location = (
                my_team_details.get("location")
                if result.venue == "home"
                else opp_team_details.get("location")
            )

            self.add_match_to_table(result, my_team_details, opp_team_details)

        self.print_match_table()

        if not self.results_manager.results:
            print("No results found.")

    def _print_table_header(self) -> None:
        """print the header row"""
        self.table.add_column("R")
        self.table.add_column("venue")
        self.table.add_column("Us")
        self.table.add_column("Op")
        self.table.add_column("opp")
        self.table.add_column("date")
        self.table.add_column("note")

    def add_match_to_table(self, result: LeagueResult, me: Team, opp: Team) -> None:
        """format this result as a line in the table"""
        self.table.add_row(
                result.result,
                result.venue,
                str(result.our_score),
                str(result.opp_score),
                opp.get('name'),
                result.match_date().strftime('%Y-%m-%d %H:%M'),
                result.notes(),
        )

    def print_match_table(self) -> None:
        self.console.print(self.table)


def main() -> None:
    """
    Main entry point of the script.
    """
    parser = argparse.ArgumentParser(description="Team League Results Manager")
    parser.add_argument("--results-file",
                        help="YAML file containing the results")
    parser.add_argument("--teams-file",
                        help="YAML file containing the team details")
    args = parser.parse_args()

    results_filename = args.results_file or env.str("RESULTS_FILE")
    teams_filename = args.teams_file or env.str("TEAMS_FILE")

    results_manager = LeagueResultsManager.from_yaml(results_filename)
    teams_manager = TeamManager.from_yaml(teams_filename)

    printer = ResultsTablePrinter(results_manager, teams_manager)
    printer.print()


if __name__ == "__main__":
    main()
