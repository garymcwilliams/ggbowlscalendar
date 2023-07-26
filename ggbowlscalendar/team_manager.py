"""
Team League Results Management System

"""

from dataclasses import dataclass
from typing import List


@dataclass
class TeamData:
    """basic Team data"""
    name: str
    location: str
    depart: int


class Team:
    """Represents a team."""

    def __init__(self, team_id: str, name: str, location: str,
                 depart: int) -> None:
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
        self.depart = depart


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
                        location=team_data["location"],
                        depart=team_data.get("depart", 60))
            teams.append(team)

        return cls(teams)

    def get_team_details(self, team_id: str) -> TeamData:
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
            return TeamData(team.name, team.location, team.depart)
        return TeamData(f"***{team_id}***", "TBD", 0)
