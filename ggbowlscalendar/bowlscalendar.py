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
results:
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
  address: Address B

Opponent C:
  name: Team C
  address: Address C
"""

import yaml
from typing import Any, List
from envparse import env
import argparse
from match_printer import print_table_header, print_match_table, add_match_to_table


class LeagueResult:
    """Represents a single league result."""

    def __init__(
        self,
        venue: str,
        opp_id: str,
        date: str,
        our_score: int,
        opp_score: int,
        newdate: str = None,
    ):
        """
        Initialize a LeagueResult instance.

        Args:
            venue (str): The venue associated with the result.
            opp_id (str): The ID of the opponent team.
            date (str): The original date of the match.
            our_score (int): The score of our team.
            opp_score (int): The score of the opponent team.
            newdate (str, optional): The new date of the match (if available).
        """
        self.venue = venue
        self.opp_id = opp_id
        self.date = date
        self.our_score = our_score
        self.opp_score = opp_score
        self.newdate = newdate
        self.result = "W" if our_score > opp_score else "L" if our_score < opp_score else "D"

    def match_date(self) -> str:
        """
        Get the match date of the result.

        Returns:
            str: The match date.
        """
        return self.newdate if self.newdate else self.date


class LeagueResultsManager:
    """Manages a team league results."""

    me = None
    duration = None

    def __init__(self, results: List[LeagueResult]):
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

        LeagueResultsManager.me = data.get("me", None)
        LeagueResultsManager.duration = data.get("duration", None)
        results_data = data.get("results", [])
        results = []
        for result_data in results_data:
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

            result = LeagueResult(venue, opp_id, date, our_score, opp_score, newdate)
            results.append(result)

        return cls(results)

    def display_results(self, team_manager: "TeamManager") -> None:
        """
        Display the league results.

        Args:
            team_manager (TeamManager): The team manager containing the team details.
        """

        print_table_header()

        for result in self.results:
            me_team_details = team_manager.get_team_details(LeagueResultsManager.me)
            opp_team_details = team_manager.get_team_details(result.opp_id)

            address = me_team_details.get('address') if result.venue == "home" else opp_team_details.get('address')

            add_match_to_table(
                result.result,
                result.venue,
                result.match_date(),
                me_team_details.get('name'),
                result.our_score,
                result.opp_score,
                opp_team_details.get('name'),
            )

        print_match_table()

        if not self.results:
            print("No results found.")


class Team:
    """Represents a team."""

    def __init__(self, id: str, name: str, address: str):
        """
        Initialize a Team instance.

        Args:
            id (str): The ID of the team.
            name (str): The name of the team.
            address (str): The address of the team.
        """
        self.id = id
        self.name = name
        self.address = address


class TeamManager:
    """Manages the team details."""

    def __init__(self, teams: List[Team]):
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
            team = Team(id=team_id, name=team_data["name"], address=team_data["address"])
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
            return {"name": team.name, "address": team.address}
        return {}


def main():
    """
    Main entry point of the script.
    """
    parser = argparse.ArgumentParser(description="Team League Results Manager")
    parser.add_argument("--results-file", help="YAML file containing the results")
    parser.add_argument("--teams-file", help="YAML file containing the team details")
    args = parser.parse_args()

    results_filename = args.results_file or env.str("RESULTS_FILE")
    teams_filename = args.teams_file or env.str("TEAMS_FILE")

    results_manager = LeagueResultsManager.from_yaml(results_filename)
    teams_manager = TeamManager.from_yaml(teams_filename)

    results_manager.display_results(teams_manager)


if __name__ == "__main__":
    main()
