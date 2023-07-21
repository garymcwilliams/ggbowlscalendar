"""
Created on 11 Oct 2017

@author: gmcwilliams
"""
from datetime import datetime, timedelta
from pathlib import Path
from .match_printer import print_header, print_matches, add_match

import strictyaml
from icalendar import Alarm, Calendar
from icalendar.cal import Event

from .match import Match
from .utils import get_match_file, get_team_file, savedir


class Events:
    """
    Manage calendar events. Includes methods for dealing with a set of matches
    for a year.
    """

    def __init__(self, club, year):
        """
        Initialise.

        This will look for files beginning with the club name
        in the data folder. club_teams will define the shorthand for each
        opponent as well as their google maps location. club_fixtures will
        define the fixtures and date as well as recording the scores for
        matches as they are played.

        :param club: String name of the club
        :param year: String year to look for matches, e.g. 2017-18
        """

        self.savedir = savedir()

        self.club = club
        if self.club.startswith("fallsoutdoor") \
                or self.club.startswith("fallsmidweek"):
            clubdata = "fallsoutdoor"
        else:
            clubdata = club
        self.year = year

        self.cal = Calendar()
        self.cal.add("prodid", "-//Bowling Calendar//mc-williams.co.uk//")
        self.cal.add("version", "2.0")
        self.cal.add("calscale", "GREGORIAN")
        self.cal.add("X-WR-TIMEZONE", "Europe/London")

        matchfile = get_match_file(club, year)
        matchdata = self._load_data(matchfile)
        self.myclub = matchdata["me"]
        self.default_start_time = matchdata["start_time"]
        self.duration = float(matchdata["duration"])
        self.matches = matchdata["matches"]

        teamfile = get_team_file(clubdata)
        teamdata = self._load_data(teamfile, None)
        self.team_data = teamdata["teams"]

    def add_events(self):
        """Add all events for this team / season to the calendar"""

        print_header()

        for match in self.matches:
            match_date = match["date"]
            # match will be defined as "home": "Opponent" meaning WE are HOME
            # against the Opponent, so some of the following will appear to be
            # processed back to front (or home to away)
            if "home" in match:
                home_id = self.myclub
                home_score = match["our_score"]
                away_id = match["home"]
                away_score = match["opp_score"]
            else:
                home_id = match["away"]
                home_score = match["opp_score"]
                away_id = self.myclub
                away_score = match["our_score"]

            location = ""
            warning = ""
            start_time = self.default_start_time

            if home_id in self.team_data:
                home_team_data = self.team_data[home_id]
                home_team_name = home_team_data["name"]
                location = home_team_data["location"]
                if "start_time" in home_team_data:
                    start_time = home_team_data["start_time"]
            else:
                warning = "****"
                home_team_name = home_id

            if "location" in match:
                location_data = self.team_data[match["location"]]
                location = location_data["location"]

            if "start_time" in match:
                start_time = match["start_time"]

            if away_id in self.team_data:
                away_team_data = self.team_data[away_id]
                away_team_name = away_team_data["name"]
            else:
                warning = "****"
                away_team_name = away_id

            duration = self.duration
            if "duration" in match:
                duration = match["duration"]

            label = None
            if "label" in match:
                label = match["label"]

            new_date = None
            if "newdate" in match:
                new_date = match["newdate"]

            new_time = None
            if "newtime" in match:
                new_time = match["newtime"]

            home_team_name = home_team_name.data
            away_team_name = away_team_name.data
            if "team" in match:
                if home_id != self.myclub:
                    home_team_name = f"{home_team_name} {match['team']}"
                else:
                    away_team_name = f"{away_team_name} {match['team']}"

            match = Match(
                myclub=self.myclub.data,
                home_team_id=home_id.data,
                home_team_name=home_team_name,
                home_score=home_score.data,
                away_team_id=away_id.data,
                away_team_name=away_team_name,
                away_score=away_score.data,
                date=match_date,
                time=start_time,
                location=location,
                warning=warning,
                duration=duration,
                label=label,
                new_date=new_date,
                new_time=new_time,
            )

            # 32: If new_date is "" then don't add event, but still print
            # match content
            if new_date != "":
                self.cal.add_component(self._create_event(match))

            add_match(match)

        print_matches()
        # self._print_cal()
        self._write_file()

    def _load_data(self, filename: str, schema=None):
        "loads the data file"
        with open(filename, "r") as data_file:
            ymldata = data_file.read()
            data = strictyaml.load(ymldata, schema)
        return data

    def _create_event(self, match):
        """
        Creates a calendar event for the given match

        :param match: A Match object holding the match data
        """
        #    print(self.team_data)
        #    print(team_data)

        event = Event()
        event["uid"] = match.id()
        event["location"] = match.location
        event.add("priority", 5)

        event.add("summary", match.summary())
        event.add("description", str(match))
        event.add("dtstart", match.match_start)
        event.add("dtend", match.match_end)
        event.add("dtstamp", datetime.utcnow())

        alarm = Alarm()
        alarm.add("action", "DISPLAY")
        alarm.add("description", "Reminder")
        alarm.add("trigger", timedelta(hours=-1))
        event.add_component(alarm)

        return event

    def _mk_save_dir(self) -> Path:
        newdir = Path(self.savedir / "Apps" / "icalendar")

        if not newdir.exists():
            newdir.mkdir(parents=True)

        return newdir

    def _write_file(self):
        filename = f"{self.club}_{self.year}.ics"
        newfile = self._mk_save_dir() / filename
        newfile.write_bytes(self.cal.to_ical())
        print(f"saved:{newfile}")

    def _print_cal(self):
        print(self.cal.to_ical())
