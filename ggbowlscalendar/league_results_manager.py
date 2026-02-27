"""
Team League Results Management System
"""

from datetime import datetime as dt
from datetime import time as dt_time
from datetime import date as dt_date
from datetime import timedelta
from typing import List


TBD_DATA = "tbd"  # data value the represents TBD match date
TBD_DISPLAY = "-date-TBD-"  # value to display in outpu for TBD match date


class LeagueResult:
    """Represents a single league result."""

    def __init__(
        self,
        venue: str,
        opp_id: str,
        date: dt_date,
        time: str,
        our_score: int,
        opp_score: int,
        newdate: dt_date | None = None,
        new_time: str | None = None,
        sub_team: str | None = None,
        label: str = "",
        location: str | None = None,
    ):
        """
        Initialize a LeagueResult instance.

        Args:
            venue (str): The venue associated with the result.
            opp_id (str): The ID of the opponent team.
            date (dt_date): The original date of the match.
            time (str): The original time of the match.
            our_score (int): The score of our team.
            opp_score (int): The score of the opponent team.
            newdate (str, optional): The new date of the match (if available).
            new_time (str, optional): The new time of the match (if available).
            sub_team (str, optional): Defines if this is A/B/C team of club we
            are playing
            label (str, optional): a bunch of text that helps define the match.
            location (str, optional): a location/venue for a neutral venue match.
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
        self.location = location

        if self.not_played_yet():
            self.result = " "
        else:
            if our_score > opp_score:
                self.result = "W"
            elif opp_score > our_score:
                self.result = "L"
            else:
                self.result = "D"

    def not_played_yet(self) -> bool:
        """determine whether the match has already been played or not"""
        return self.our_score == 0.0 and self.opp_score == 0.0

    def match_date_time(self) -> dt_date | None:
        """
        return the match date & time, allowing newdate to overide the default
        if that has been provided.
        """
        match_date = self.newdate if self.newdate else self.date
        if match_date == TBD_DATA:
            return None
        time = self.new_time if self.new_time else self.time
        match_time = dt.strptime(time, '%H:%M').time()
        return dt.combine(match_date, match_time)

    def notes(self) -> str:
        """ return any special notes for printing """
        notes = self.label
        return notes

    def is_home(self) -> bool:
        """is match played at home?"""
        return self.venue == "home"

    def is_away(self) -> bool:
        """is match played away?"""
        return self.venue == "away"

    def _format_score(self, score: float) -> str | None:
        """convert float to str, strip .0 if we have integer"""
        return (
                None if self.not_played_yet()
                else f"{score:.1f}".rstrip('0').rstrip('.')
        )

    def format_our_score(self) -> str | None:
        """convert our_score to output format"""
        return self._format_score(self.our_score)

    def format_opp_score(self) -> str:
        """convert opp_score to output format"""
        return self._format_score(self.opp_score)


class LeagueResultsManager:
    """Manages a team league results."""

    def __init__(self,
                 my_team_id: str,
                 duration: int,
                 default_day: str,
                 results: List[LeagueResult]) -> None:
        """
        Initialize a LeagueResultsManager instance.

        Args:
            my_team_id (str): what id represents my team in this league.
            duration: (int): the default duration in hours of a match in this
            league.
            results (List[LeagueResult]): The list of league results.
        """

        self.my_team_id : str = my_team_id
        self.duration : int = duration
        self.default_day = default_day
        self.results = results

    @classmethod
    def from_dict(cls, data: dict) -> "LeagueResultsManager":
        """
        Create a LeagueResultsManager instance from YAML data.

        Args:
            date: the YAML data

        Returns:
            LeagueResultsManager: The created LeagueResultsManager instance.
        """
        my_team_id = data.get("me")
        duration = data.get("duration")
        default_time = data.get("start_time")
        default_day = data.get("day")

        matches_data = data.get("matches", [])
        matches = []
        for result_data in matches_data:
            if "home" in result_data:
                venue = "home"
                opp_id = result_data["home"]
            else:
                venue = "away"
                opp_id = result_data["away"]

            date = result_data.get("date")
            newdate = result_data.get("newdate")
            new_time = result_data.get("newtime")
            our_score = result_data.get("our_score", 0)
            opp_score = result_data.get("opp_score", 0)
            sub_team = result_data.get("team", None)
            label = result_data.get("label", "")
            location = result_data.get("location", None)
            start_time = result_data.get("start_time", default_time)

            result = LeagueResult(venue, opp_id, date, start_time, our_score,
                                  opp_score, newdate, new_time, sub_team,
                                  label, location)
            matches.append(result)

        return cls(my_team_id, duration, default_day, matches)
