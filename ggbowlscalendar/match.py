"""
Created on 19 Jun 2018

@author: gmcwilliams
"""
from datetime import timedelta, datetime


def _format_date_time(date, time) -> str:
    date_fmt_in = "%Y-%m-%d_%H:%M"
    return datetime.strptime(f"{date}_{time}", date_fmt_in)


def _calc_result(our_score: str, opp_score: str) -> str:
    ourscore = float(our_score)
    oppscore = float(opp_score)
    if ourscore == 0 and oppscore == 0:
        result = "."  # not yet played
    elif ourscore > oppscore:
        result = "W"
    elif ourscore < oppscore:
        result = "L"
    else:
        result = "D"

    return result


class Match:
    """
    Manage one match
    """

    def __init__(
        self,
        myclub,
        home_team_id,
        home_team_name,
        home_score,
        away_team_id,
        away_team_name,
        away_score,
        date,
        time,
        location,
        warning="",
        duration=3,
        label=None,
        new_date=None,
        new_time=None,
    ):

        self.myclub = myclub
        self.home_id = home_team_id
        self.home_team_name = home_team_name
        self.home_score = home_score
        self.away_id = away_team_id
        self.away_team_name = away_team_name
        self.away_score = away_score
        self.location = location
        self.warning = warning

        duration = timedelta(hours=duration)

        if myclub == home_team_id:
            self.result = _calc_result(home_score, away_score)
        else:
            self.result = _calc_result(away_score, home_score)

        self.match_date = _format_date_time(date, time)
        # for consistency, always use the original date for id, even if match
        # time moves
        self.id_time = self.match_date.strftime("%Y-%m-%d")
        if new_date is not None and new_date != "":
            if new_time is not None:
                self.match_date = _format_date_time(new_date, new_time)
            else:
                self.match_date = _format_date_time(new_date, time)

        self.match_end = self.match_date + duration
        # expect to arrive 10 mins early
        self.match_start = self.match_date - timedelta(minutes=10)

        self.label = ""
        if label is not None:
            self.label = f" {label}"
        if new_date == "":
            self.label = " ****-TBD-****"

    def summary(self) -> str:
        """Return match summary in pre-defined format"""
        return (
            f"{self.home_team_name} ({self.home_score})"
            f" v "
            f"({self.away_score}) {self.away_team_name}"
            f"{self.label}"
        )

    def _display_date(self):
        # display_date = self.match_start.strftime(self.date_fmt_in)
        return self.match_date.strftime("%Y-%m-%d@%H:%M")

    def description(self):
        """
        Return the match data in the defined format as a description
        """
        return (
            f"{self.result:1s} "
            f"{self.home_team_name} "
            f"({self.home_score}) "
            "v "
            f"({self.away_score}) "
            f"{self.away_team_name} "
            f"{self._display_date()}"
            f"{self.label}"
        )

    # TODO #56 print_description should return csv and let caller do the formatting
    def print_description(self):
        """
        Return a well-formatted, aligned, description of the match, suitable
        for printing
        """
        return (
            f"{self.result:1s} "
            f"{self.home_team_name:15s} ({self.home_score:3})"
            # #56 don't return the v, let caller do all formatting
            f" v "
            f"({self.away_score:3}) {self.away_team_name:15s} "
            f"{self._display_date()}"
            f"{self.label} "
            f"{self.warning}"
        ).strip()

    def id(self) -> str:
        """Define a Unique ID for the match."""

        # if we move match times, e.g. a cup game, then we cannot use simply
        # the time, otherwise both the original and the new game will have same
        # ID, so need to add the clubname
        id_team = self.home_id
        if self.home_id == self.myclub:
            id_team = self.away_id
        id_team = id_team.replace(" ", "")
        return (
            f"{self.myclub.replace(' ','')}-"
            f"{self.id_time}-"
            f"{id_team}"
            f"@mc-williams.co.uk"
        )

    def __repr__(self):
        return (
            f"{self.home_team_name!r},({self.home_score!r}),"
            "({self.away_score!r}),{self.away_team_name!r},"
            "{self.match_date!r},{self.label!r}"
        )

    def __str__(self) -> str:
        """
        Return the match data in the defined format as a description
        """
        return (
            f"{self.home_team_name} ({self.home_score})"
            f" v "
            f"({self.away_score}) {self.away_team_name}"
            f" on "
            f"{self.match_date} {self.label}"
        )
