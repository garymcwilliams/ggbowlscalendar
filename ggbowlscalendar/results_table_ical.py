from datetime import datetime, timedelta
from icalendar import Alarm, Calendar
from icalendar.cal import Event

from .league_results_manager import LeagueResultsManager, LeagueResult
from .team_manager import TeamManager
from .utils import write_file


def _print_cal(self):
    print(self.cal.to_ical())


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

    def summary(self, result: LeagueResult, opp_team_details: dict) -> str:
        """Return match summary in pre-defined format"""
        return (
            f"{result.result} "
            f"{result.match_date().strftime('%Y-%m-%d %H:%M')} "
            f"{result.venue} "
            f"{str(result.our_score)} v "
            f"{str(result.opp_score)} {opp_team_details['name']} "
            f"{result.notes()}"
        )

    def match_desc(self, result: LeagueResult, opp_team_details: dict) -> str:
        """Return match header description."""
        return (
            f"{result.result} "
            f"{result.match_date().strftime('%Y-%m-%d %H:%M')} "
            f"{result.venue} "
            f"{str(result.our_score)} v "
            f"{str(result.opp_score)} {opp_team_details['name']} "
            f"{result.notes()}"
        )

    def generate_ical(self) -> None:
        """ generate the ical entries.  """

        self._create_header()

        for result in self.results_manager.results:
            opp_team_details = self.team_manager.get_team_details(
                result.opp_id
            )

            self._add_event(result, opp_team_details)

        if not self.results_manager.results:
            print("No results found.")
        else:
            write_file(self.results_manager.my_team_id, "2029",
                       self.cal.to_ical())

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

        id_time = result.date.strftime("%Y%m%d%H%M")

        return (
            f"{self.results_manager.my_team_id.replace(' ','')}-"
            f"{id_time}"
            f"{label}"
            f"@mc-williams.co.uk"
        )

    def _create_header(self) -> None:
        """create the calendar header content."""
        self.cal.add("prodid", "-//Bowling Calendar//mc-williams.co.uk//")
        self.cal.add("version", "2.0")
        self.cal.add("calscale", "GREGORIAN")
        self.cal.add("X-WR-TIMEZONE", "Europe/London")

    def _add_event(self, result: LeagueResult, opp_team_details: dict) -> None:
        """
        Creates a calendar event for the given match

        :param match: A Match object holding the match data
        """
        #    print(self.team_data)
        #    print(team_data)

        # 32: If new_date is "" then don't add event
        if result.newdate == "":
            return

        location = self.my_team_details.get("location") \
            if result.venue == "home" \
            else opp_team_details.get("location")

        match_start = result.match_date() - timedelta(minutes=10)
        match_end = result.match_date() + timedelta(hours=self.results_manager.duration)

        event = Event()
        event["uid"] = self._calendar_id(result)
        event["location"] = location
        event.add("priority", 5)

        event.add("summary", self.summary(result, opp_team_details))
        event.add("description", self.match_desc(result, opp_team_details))
        event.add("dtstart", match_start)
        event.add("dtend", match_end)
        event.add("dtstamp", datetime.utcnow())

        alarm = Alarm()
        alarm.add("action", "DISPLAY")
        alarm.add("description", "Reminder")
        alarm.add("trigger", timedelta(hours=-1))
        event.add_component(alarm)

        self.cal.add_component(event)
