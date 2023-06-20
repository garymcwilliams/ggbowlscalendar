"""
Team League Results Management System

"""

from pathlib import Path
from typing import List

import yaml

from .utils import find_file


def get_teams_file() -> Path:
    """
    Get the teams Path
    """
    return find_file(None, "teams.yml")


class Team:
    """Represents a team."""

    def __init__(self, team_id: str, name: str, location: str) -> None:
        """
        Initialize a Team instance.

        Args:
            id (str): The ID of the team.
            name (str): The name of the team.
            location (str): The location of the team.
        """
        self.team_id = team_id
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
    def from_yaml(cls) -> "TeamManager":
        """
        Create a TeamManager instance from a YAML file.

        Args:
            filename (str): The filename of the YAML file.

        Returns:
            TeamManager: The created TeamManager instance.
        """
        file_path = get_teams_file()
        with open(file_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        print(data)

        return TeamManager.from_dict(data)

    @classmethod
    def from_dict(cls, data: dict) -> "TeamManager":
        """
        Create a TeamManager instance from YAML data.

        Args:
            date: the YAML data

        Returns:
            TeamManager: The created TeamManager instance.
        """
        teams = []
        for team_id, team_data in data.items():
            team = Team(team_id=team_id, name=team_data["name"],
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
        team = next((team for team in self.teams if team.team_id == team_id),
                    None)
        if team:
            return {"name": team.name, "location": team.location}
        return {"name": f"***{team_id}***", "location": "TBD"}
