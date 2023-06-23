"""
Team League Results Management System
"""

import datetime
from typing import List


TBD_DATA = "tbd"  # data value the represents TBD match date
TBD_DISPLAY = "-date-TBD-"  # value to display in outpu for TBD match date


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
            sub_team (str, optional): Defines if this is A/B/C team of club we
            are playing
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
        return (
                True if self.our_score == 0.0 and self.opp_score == 0.0
                else False
        )

    def match_date_time(self) -> datetime:
        """
        return the match date & time, allowing newdate to overide the default
        if that has been provided.
        """
        match_date = self.newdate if self.newdate else self.date
        if self.newdate == TBD_DATA:
            self.label += TBD_DISPLAY
            return None
        time = self.new_time if self.new_time else self.time
        match_time = datetime.datetime.strptime(time, '%H:%M').time()
        match_date_time = datetime.datetime.combine(match_date, match_time)

        return match_date_time

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

    def _format_score(self, score: float) -> str:
        """convert float to str, strip .0 if we have integer"""
        return (
                None if self.not_played_yet()
                else f"{score:.1f}".rstrip('0').rstrip('.')
        )

    def format_our_score(self) -> str:
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

        self.my_team_id = my_team_id
        self.duration = duration
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
            start_time = (
                result_data["start_time"]
                if "start_time" in result_data
                else default_time
            )

            result = LeagueResult(venue, opp_id, date, start_time, our_score,
                                  opp_score, newdate, new_time, sub_team,
                                  label)
            matches.append(result)

        return cls(my_team_id, duration, default_day, matches)
