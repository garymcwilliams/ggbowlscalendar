"""
test
"""
import datetime
from ggbowlscalendar.results_table_ical import ResultsTableIcal
from ggbowlscalendar.league_results_manager import LeagueResultsManager
from ggbowlscalendar.team_manager import TeamManager


DATE1 = datetime.datetime.strptime("2023-04-22", '%Y-%m-%d')
UTCNOW = datetime.datetime.now(datetime.timezone.utc)


class TestResultsTableIcal:
    """
    Tests
    """

    def test_lost_away(self):
        """
        tests
        """

        match_dict = {
            'me': 'FALLSA',
            'start_time': '14:00',
            'day': 'Sat',
            'duration': 3,
            'matches':
                [
                    {
                        'away': 'CLIFT',
                        'date': DATE1,
                        'our_score': 0.5,
                        'opp_score': 5.5,
                    },
                ]
        }

        results_manager = LeagueResultsManager.from_dict(match_dict)

        team_dict = {
            'FALLSA': {'name': 'AAAA', 'location': 'AAA location'},
            'CLIFT': {'name': 'clift', 'location': 'clift location'}
        }

        team_manager = TeamManager.from_dict(team_dict)

        ical_generator = ResultsTableIcal(results_manager, team_manager)
        for result in results_manager.results:
            opp_team_details = team_manager.get_team_details(
                result.opp_id
            )

            event = ical_generator._create_event(result,
                                                 opp_team_details,
                                                 UTCNOW)
            assert event.get('UID') == 'FALLSA-202304221400@mc-williams.co.uk'
            assert event.get('LOCATION') == 'clift location'
            assert event.get('SUMMARY') == 'AAAA L (0.5)(5.5) v clift away'
            assert event.get('DESCRIPTION') == 'L away (clift)'

    def test_lost_home(self):
        """
        tests
        """

        match_dict = {
            'me': 'FALLSA',
            'start_time': '14:00',
            'day': 'Sat',
            'duration': 3,
            'matches':
                [
                    {
                        'home': 'CLIFT',
                        'date': DATE1,
                        'our_score': 1,
                        'opp_score': 6,
                    },
                ]
        }

        results_manager = LeagueResultsManager.from_dict(match_dict)

        team_dict = {
            'FALLSA': {'name': 'AAAA', 'location': 'AAA location'},
            'CLIFT': {'name': 'clift', 'location': 'clift location'}
        }

        team_manager = TeamManager.from_dict(team_dict)

        ical_generator = ResultsTableIcal(results_manager, team_manager)
        for result in results_manager.results:
            opp_team_details = team_manager.get_team_details(
                result.opp_id
            )

            event = ical_generator._create_event(result,
                                                 opp_team_details,
                                                 UTCNOW)
            assert event.get('UID') == 'FALLSA-202304221400@mc-williams.co.uk'
            assert event.get('LOCATION') == 'AAA location'
            assert event.get('SUMMARY') == 'AAAA L (1)(6) v clift home'
            assert event.get('DESCRIPTION') == 'L home (clift)'

    def test_won_away(self):
        """
        tests
        """

        match_dict = {
            'me': 'FALLSA',
            'start_time': '14:00',
            'day': 'Sat',
            'duration': 3,
            'matches':
                [
                    {
                        'away': 'CLIFT',
                        'date': DATE1,
                        'our_score': 6,
                        'opp_score': 1,
                    },
                ]
        }

        results_manager = LeagueResultsManager.from_dict(match_dict)

        team_dict = {
            'FALLSA': {'name': 'AAAA', 'location': 'AAA location'},
            'CLIFT': {'name': 'clift', 'location': 'clift location'}
        }

        team_manager = TeamManager.from_dict(team_dict)

        ical_generator = ResultsTableIcal(results_manager, team_manager)
        for result in results_manager.results:
            opp_team_details = team_manager.get_team_details(
                result.opp_id
            )

            event = ical_generator._create_event(result,
                                                 opp_team_details,
                                                 UTCNOW)
            assert event.get('UID') == 'FALLSA-202304221400@mc-williams.co.uk'
            assert event.get('LOCATION') == 'clift location'
            assert event.get('SUMMARY') == 'AAAA W (6)(1) v clift away'
            assert event.get('DESCRIPTION') == 'W away (clift)'

    def test_won_home(self):
        """
        tests
        """

        match_dict = {
            'me': 'FALLSA',
            'start_time': '14:00',
            'day': 'Sat',
            'duration': 3,
            'matches':
                [
                    {
                        'home': 'CLIFT',
                        'date': DATE1,
                        'our_score': 6,
                        'opp_score': 1,
                    },
                ]
        }

        results_manager = LeagueResultsManager.from_dict(match_dict)

        team_dict = {
            'FALLSA': {'name': 'AAAA', 'location': 'AAA location'},
            'CLIFT': {'name': 'clift', 'location': 'clift location'}
        }

        team_manager = TeamManager.from_dict(team_dict)

        ical_generator = ResultsTableIcal(results_manager, team_manager)
        for result in results_manager.results:
            opp_team_details = team_manager.get_team_details(
                result.opp_id
            )

            event = ical_generator._create_event(result,
                                                 opp_team_details,
                                                 UTCNOW)
            assert event.get('UID') == 'FALLSA-202304221400@mc-williams.co.uk'
            assert event.get('LOCATION') == 'AAA location'
            assert event.get('SUMMARY') == 'AAAA W (6)(1) v clift home'
            assert event.get('DESCRIPTION') == 'W home (clift)'

    def test_won_label(self):
        """
        tests
        """

        match_dict = {
            'me': 'FALLSA',
            'start_time': '14:00',
            'day': 'Sat',
            'duration': 3,
            'matches':
                [
                    {
                        'home': 'CLIFT',
                        'label': 'Irish Cup',
                        'date': DATE1,
                        'our_score': 6,
                        'opp_score': 1,
                    },
                ]
        }

        results_manager = LeagueResultsManager.from_dict(match_dict)

        team_dict = {
            'FALLSA': {'name': 'AAAA', 'location': 'AAA location'},
            'CLIFT': {'name': 'clift', 'location': 'clift location'}
        }

        team_manager = TeamManager.from_dict(team_dict)

        ical_generator = ResultsTableIcal(results_manager, team_manager)
        for result in results_manager.results:
            opp_team_details = team_manager.get_team_details(
                result.opp_id
            )

            event = ical_generator._create_event(result,
                                                 opp_team_details,
                                                 UTCNOW)
            assert event.get('UID') == \
                'FALLSA-202304221400IrishCup@mc-williams.co.uk'
            assert event.get('LOCATION') == 'AAA location'
            assert event.get('SUMMARY') == \
                'AAAA W (6)(1) v clift home Irish Cup'
            assert event.get('DESCRIPTION') == 'W home (clift)'

    def test_not_played_yet(self):
        """
        tests
        """

        match_dict = {
            'me': 'FALLSA',
            'start_time': '14:00',
            'day': 'Sat',
            'duration': 3,
            'matches':
                [
                    {
                        'home': 'CLIFT',
                        'label': 'Irish Cup',
                        'date': DATE1,
                        'our_score': 0,
                        'opp_score': 0,
                    },
                ]
        }

        results_manager = LeagueResultsManager.from_dict(match_dict)

        team_dict = {
            'FALLSA': {'name': 'AAAA', 'location': 'AAA location'},
            'CLIFT': {'name': 'clift', 'location': 'clift location'}
        }

        team_manager = TeamManager.from_dict(team_dict)

        ical_generator = ResultsTableIcal(results_manager, team_manager)
        for result in results_manager.results:
            opp_team_details = team_manager.get_team_details(
                result.opp_id
            )

            event = ical_generator._create_event(result,
                                                 opp_team_details,
                                                 UTCNOW)
            assert event.get('UID') == \
                'FALLSA-202304221400IrishCup@mc-williams.co.uk'
            assert event.get('LOCATION') == 'AAA location'
            assert event.get('SUMMARY') == 'AAAA v (clift) home Irish Cup'
            assert event.get('DESCRIPTION') == 'home (clift)'

    def test_ical_generator(self):
        """
        tests
        """

        match_dict = {
            'me': 'FALLSA',
            'start_time': '14:00',
            'day': 'Sat',
            'duration': 3,
            'matches':
                [
                    {
                        'home': 'CLIFT',
                        'label': 'Irish Cup',
                        'date': DATE1,
                        'our_score': 0,
                        'opp_score': 0,
                    },
                ]
        }

        results_manager = LeagueResultsManager.from_dict(match_dict)

        team_dict = {
            'FALLSA': {'name': 'AAAA', 'location': 'AAA location'},
            'CLIFT': {'name': 'clift', 'location': 'clift location'}
        }

        dtstamp = UTCNOW.strftime('%Y%m%dT%H%M%SZ')
        ical_content = (
                        "BEGIN:VCALENDAR\r\n"
                        "VERSION:2.0\r\n"
                        "PRODID:-//Bowling Calendar//mc-williams.co.uk//\r\n"
                        "CALSCALE:GREGORIAN\r\n"
                        "X-WR-TIMEZONE:Europe/London\r\n"
                        "BEGIN:VEVENT\r\n"
                        "SUMMARY:AAAA v (clift) home Irish Cup\r\n"
                        "DTSTART;VALUE=DATE-TIME:20230422T135000\r\n"
                        "DTEND;VALUE=DATE-TIME:20230422T170000\r\n"
                        f"DTSTAMP;VALUE=DATE-TIME:{dtstamp}\r\n"
                        "UID:FALLSA-202304221400IrishCup@mc-williams.co.uk\r\n"
                        "DESCRIPTION:home (clift)\r\n"
                        "LOCATION:AAA location\r\n"
                        "PRIORITY:5\r\n"
                        "BEGIN:VALARM\r\n"
                        "ACTION:DISPLAY\r\n"
                        "DESCRIPTION:Reminder\r\n"
                        "TRIGGER:-PT1H\r\n"
                        "END:VALARM\r\n"
                        "END:VEVENT\r\n"
                        "END:VCALENDAR\r\n"
                        )

        team_manager = TeamManager.from_dict(team_dict)

        ical_generator = ResultsTableIcal(results_manager, team_manager)
        ical_generator.generate_ical()
        bytes = ical_generator.cal.to_ical()
        assert bytes == ical_content.encode()
