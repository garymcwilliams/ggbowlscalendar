"""
Team League Results Management System
"""

import datetime
from typing import List

import yaml

from utils import get_games_file


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
        new_time: str = None,
        sub_team: str = None,
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
            new_time (str, optional): The new time of the match (if available).
            sub_team (str, optional): Defines if this is A/B/C team of club we are playing
            label (str, optional): a bunch of text that helps define the match.
        """
        self.venue = venue
        self.opp_id = opp_id
        self.sub_team = sub_team
        self.date = date
        self.time = time
        self.our_score = float(our_score)
        self.opp_score = float(opp_score)
        self.newdate = newdate
        self.new_time = new_time
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
        time = self.new_time if self.new_time else self.time
        match_time = datetime.datetime.strptime(time, '%H:%M').time()
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
    def from_yaml(cls, team: str, year: str) -> "LeagueResultsManager":
        """
        Create a LeagueResultsManager instance from a YAML file.

        Args:
            filename (str): The filename of the YAML file.

        Returns:
            LeagueResultsManager: The created LeagueResultsManager instance.
        """
        file = get_games_file(team, year)

        with open(file, "r", encoding="utf-8") as file:
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
            new_time = result_data.get("newtime")
            our_score = result_data.get("our_score", 0)
            opp_score = result_data.get("opp_score", 0)
            sub_team = result_data.get("team", None)
            label = result_data.get("label", "")
            start_time = (
                result_data["start_time"]
                if "start_time" in result_data
                else default_time
            )

            result = LeagueResult(venue, opp_id, date, start_time, our_score,
                                  opp_score, newdate, new_time, sub_team,
                                  label)
            matches.append(result)

        return cls(me, duration, matches)
