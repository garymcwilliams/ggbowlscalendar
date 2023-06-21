"""
test
"""
import datetime
from ggbowlscalendar.league_results_manager import LeagueResultsManager

DATE1 = '2023-04-22'
DATE2 = '2023-04-30'


def combine_date_time(date: datetime, time: str):
    """combine date and time"""
    calc_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    calc_time = datetime.datetime.strptime(time, '%H:%M').time()
    return datetime.datetime.combine(calc_date, calc_time)


class TestLeagueResultsManager:
    """
    Tests
    """

    def test_default_content(self):
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
                    {'away': 'CLIFT',
                     'date': datetime.datetime.strptime(DATE1, '%Y-%m-%d'),
                     'our_score': 0.5,
                     'opp_score': 5.5,
                    },
                ]
        }

        results_manager = LeagueResultsManager.from_dict(match_dict)
        assert results_manager.default_day == 'Sat'
        assert results_manager.duration == 3
        assert len(results_manager.results) == 1

    def test_match_home(self):
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
                    {'home': 'CLIFT',
                     'date': datetime.datetime.strptime(DATE1, '%Y-%m-%d'),
                     'our_score': 0.5,
                     'opp_score': 5.5,
                    },
                ]
        }

        results_manager = LeagueResultsManager.from_dict(match_dict)
        match = results_manager.results[0]
        assert match.is_home()
        assert match.result == 'L'
        assert match.notes() == ""
        assert match.format_our_score() == "0.5"
        assert match.format_opp_score() == "5.5"
        assert match.match_date_time() == combine_date_time(DATE1, "14:00")

    def test_match_away(self):
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
                    {'away': 'CLIFT',
                     'date': datetime.datetime.strptime(DATE1, '%Y-%m-%d'),
                     'our_score': 0.5,
                     'opp_score': 5.5,
                    },
                ]
        }

        results_manager = LeagueResultsManager.from_dict(match_dict)
        match = results_manager.results[0]
        assert match.is_away()
        assert match.result == 'L'
        assert match.notes() == ""
        assert match.match_date_time() == combine_date_time(DATE1, "14:00")

    def test_match_not_yet_played(self):
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
                    {'away': 'CLIFT',
                     'date': datetime.datetime.strptime(DATE1, '%Y-%m-%d'),
                     'our_score': 0.0,
                     'opp_score': 0.0,
                    },
                ]
        }

        results_manager = LeagueResultsManager.from_dict(match_dict)
        match = results_manager.results[0]
        assert match.result == ' '
        assert match.format_our_score() is None
        assert match.format_opp_score() is None

    def test_match_label(self):
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
                    {'away': 'CLIFT',
                     'date': datetime.datetime.strptime(DATE1, '%Y-%m-%d'),
                     'label': 'LABELDATA',
                     'our_score': 5.0,
                     'opp_score': 2.0,
                    },
                ]
        }

        results_manager = LeagueResultsManager.from_dict(match_dict)
        match = results_manager.results[0]
        assert match.result == 'W'
        assert match.label == "LABELDATA"
        assert match.notes() == "LABELDATA"
        assert match.format_our_score() == "5"
        assert match.format_opp_score() == "2"

    def test_match_starttime(self):
        """
        tests
        """

        time = "19:30"
        match_dict = {
            'me': 'FALLSA',
            'start_time': '14:00',
            'day': 'Sat',
            'duration': 3,
            'matches':
                [
                    {'away': 'CLIFT',
                     'date': datetime.datetime.strptime(DATE1, '%Y-%m-%d'),
                     'start_time': time,
                     'our_score': 3.5,
                     'opp_score': 3.5,
                    },
                ]
        }

        results_manager = LeagueResultsManager.from_dict(match_dict)
        match = results_manager.results[0]
        assert match.result == 'D'
        assert match.label == ""
        assert match.notes() == ""
        assert match.match_date_time() == combine_date_time(DATE1, time)

    def test_match_newtime(self):
        """
        tests
        """

        time = "18:30"
        match_dict = {
            'me': 'FALLSA',
            'start_time': '14:00',
            'day': 'Sat',
            'duration': 3,
            'matches':
                [
                    {'away': 'CLIFT',
                     'date': datetime.datetime.strptime(DATE1, '%Y-%m-%d'),
                     'newtime': time,
                     'our_score': 3.5,
                     'opp_score': 3.5,
                    },
                ]
        }

        results_manager = LeagueResultsManager.from_dict(match_dict)
        match = results_manager.results[0]
        assert match.result == 'D'
        assert match.label == ""
        assert match.notes() == ""
        assert match.match_date_time() == combine_date_time(DATE1, time)

    def test_match_newdatetime(self):
        """
        tests
        """

        time = "18:30"
        match_dict = {
            'me': 'FALLSA',
            'start_time': '14:00',
            'day': 'Sat',
            'duration': 3,
            'matches':
                [
                    {'away': 'CLIFT',
                     'date': datetime.datetime.strptime(DATE1, '%Y-%m-%d'),
                     'newdate': datetime.datetime.strptime(DATE2, '%Y-%m-%d'),
                     'newtime': time,
                     'our_score': 3.5,
                     'opp_score': 3.5,
                    },
                ]
        }

        results_manager = LeagueResultsManager.from_dict(match_dict)
        match = results_manager.results[0]
        assert match.result == 'D'
        assert match.label == ""
        assert match.notes() == ""
        assert match.match_date_time() == combine_date_time(DATE2, time)

    def test_match_nonewdatetime(self):
        """
        test if we have no date for a game
        """

        time = "18:30"
        match_dict = {
            'me': 'FALLSA',
            'start_time': '14:00',
            'day': 'Sat',
            'duration': 3,
            'matches':
                [
                    {'away': 'CLIFT',
                     'date': datetime.datetime.strptime(DATE1, '%Y-%m-%d'),
                     'newdate': 'tbd',
                     'newtime': time,
                     'our_score': 0.0,
                     'opp_score': 0.0,
                     },
                ]
        }

        results_manager = LeagueResultsManager.from_dict(match_dict)
        match = results_manager.results[0]
        assert match.match_date_time() is None
        assert match.is_away()
        assert match.not_played_yet() is True
        assert match.result == ' '
        assert match.label == "-date-TBD-"
        assert match.notes() == "-date-TBD-"
        assert match.format_our_score() is None
        assert match.format_opp_score() is None

    def test_match_not_played_yet(self):
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
                    {'home': 'CLIFT',
                     'date': datetime.datetime.strptime(DATE1, '%Y-%m-%d'),
                     'our_score': 0.0,
                     'opp_score': 0.0,
                    },
                ]
        }

        results_manager = LeagueResultsManager.from_dict(match_dict)
        match = results_manager.results[0]
        assert match.is_home()
        assert match.not_played_yet() is True
        assert match.result == ' '
        assert match.notes() == ""
        assert match.format_our_score() is None
        assert match.format_opp_score() is None
        assert match.match_date_time() == combine_date_time(DATE1, "14:00")
