"""
Generate ical for all matches
"""

import logging
from datetime import datetime, timedelta
from icalendar import Alarm, Calendar
from icalendar.cal import Event

from .league_results_manager import LeagueResultsManager, LeagueResult
from .team_manager import TeamManager, TeamData


def combine_date_time(date: datetime, time: str) -> str:
    """combine date and time, into a predefine text fotmat"""
    calc_time = datetime.strptime(time, '%H:%M').time()
    id_time = datetime.combine(date, calc_time)
    return datetime.strftime(id_time, "%Y%m%d%H%M")


class ResultsTableIcal:
    """generate ical entries for results"""

    def __init__(self,
                 results_manager: LeagueResultsManager,
                 team_manager: TeamManager) -> None:
        """
        Setup data for generating the ical entries

        Args:
            results_manager (LeagueResultsManager): The manager containing the
            results.
            team_manager (TeamManager): The team manager containing the team
            details.
        """
        self.results_manager = results_manager
        self.team_manager = team_manager
        self.my_team_details = self.team_manager.get_team_details(
            self.results_manager.my_team_id
        )
        self.cal = Calendar()
        self.logger = logging.getLogger(__name__)

    def _opp_name(self,
                  result: LeagueResult,
                  opp_team_details: TeamData) -> str:
        return (
            f"{opp_team_details.name} {result.sub_team}" if result.sub_team
            else opp_team_details.name
        )

    def summary(self, result: LeagueResult, opp_team_details: TeamData) -> str:
        """Return match summary in pre-defined format"""
        opp_name = self._opp_name(result, opp_team_details)
        summary = None
        if result.venue == 'home':
            home_name = f"{self.my_team_details.name}"
            away_name = f"({opp_name})"
        else:
            home_name = f"({opp_name})"
            away_name = f"{self.my_team_details.name}"
        match_names = f"{home_name} v {away_name}"
        if result.not_played_yet():
            summary = (
                f"{match_names} "
                f"{result.label}"
            ).rstrip()
        else:
            summary = (
                f"{match_names} "
                f"{result.result} "
                f"({result.format_our_score()} -"
                f" {result.format_opp_score()}) "
                f"{result.label}"
            ).rstrip()
        self.logger.debug("summary='%s'", summary)
        return summary

    def match_desc(self,
                   result: LeagueResult,
                   opp_team_details: TeamData) -> str:
        """Return match calendar description."""
        opp_name = self._opp_name(result, opp_team_details)
        venue = result.venue
        """if Neutral, change description of venue"""
        if result.location:
            venue = "neutral"
        desc = (
            f"{result.result} "
            f"{venue} "
            f"({opp_name})"
        )
        if desc != desc.strip():
            self.logger.debug("desc='%s' from='%s'", desc.strip(), desc)
        return desc.strip()

    def generate_ical(self, now=datetime.utcnow()) -> None:
        """
        generate the ical content. The internal 'cal' property will contain
        the generated ical events.
        """

        if not self.results_manager.results:
            print("No results found.")
            return

        self._create_header()

        for result in self.results_manager.results:
            self._add_event(result, now)

    def _calendar_id(self, result: LeagueResult) -> str:
        """
        Define a Unique ID for the match.
        The unique ID will be formed from "my" team, plus the orginal
        match date/time. We use the original date/time to allow for matches
        being rearranged. Using time is optional, but would allow for any crazy
        setup where the team would be asked to play twice in a day.
        #31 we removed the opposition name from ID to allow for Cup opponents
        being changed
        #35 using simply the date is not unique enough. We also need to account
        for any label used in the match.
        """

        label = (
            f"{result.label.replace(' ','')}" if result.label is not None
            else ""
        )

        id_time = combine_date_time(result.date, result.time)

        unique = (
            f"{self.results_manager.my_team_id.replace(' ','')}-"
            f"{id_time}"
            f"{label}"
            f"@mc-williams.co.uk"
        )
        self.logger.debug("uniqueid='%s'", unique)
        return unique

    def _create_header(self) -> None:
        """create the calendar header content."""
        self.cal.add("prodid", "-//Bowling Calendar//mc-williams.co.uk//")
        self.cal.add("version", "2.0")
        self.cal.add("calscale", "GREGORIAN")
        self.cal.add("X-WR-TIMEZONE", "Europe/London")

    def _find_location(self, result: LeagueResult,
                       opp_team_details: TeamData) -> str:
        """
        find a location.
        For a regular match, this will be the location for the home or away
        team. For a Neutral Venue game, then we will look up the location
        for the teamid set as the location for the match.
        """
        if result.location:
            neutral_team_details = self.team_manager.get_team_details(
                result.location
            )
            location = neutral_team_details.location
            self.logger.debug("neutral=%s", location)
        elif result.is_home():
            location = self.my_team_details.location
        else:
            location = opp_team_details.location

        return location

    def _create_event(self, result: LeagueResult, now: datetime) -> Event:
        match_start = result.match_date_time() - timedelta(minutes=10)
        match_end = result.match_date_time() + timedelta(
            hours=self.results_manager.duration)

        opp_team_details = self.team_manager.get_team_details(
            result.opp_id
        )
        location = self._find_location(result, opp_team_details)

        event = Event()
        event["uid"] = self._calendar_id(result)
        event["location"] = location
        event.add("priority", 5)

        event.add("summary", self.summary(result, opp_team_details))
        event.add("description", self.match_desc(result, opp_team_details))
        event.add("dtstart", match_start)
        event.add("dtend", match_end)
        event.add("dtstamp", now)
        self.logger.debug(
            "event=%s:%s:'%s':'%s'", match_start, match_end,
            event.get("summary"), event.get("description")
        )

        alarm = Alarm()
        alarm.add("action", "DISPLAY")
        alarm.add("description", "Reminder")
        alarm.add("trigger", timedelta(hours=-1))
        event.add_component(alarm)

        return event

    def _add_event(self, result: LeagueResult, now: datetime) -> None:
        """
        Creates a calendar event for the given match

        :param match: A Match object holding the match data
        """
        #    print(self.team_data)
        #    print(team_data)

        # If match has no new date, then do not add to calendar
        if result.match_date_time() is None:
            return

        event = self._create_event(result, now)

        self.cal.add_component(event)
