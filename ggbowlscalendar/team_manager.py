"""
Team League Results Management System

"""

from typing import List

import yaml

from utils import get_teams_file


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
        file = get_teams_file()
        with open(file, "r", encoding="utf-8") as file:
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
