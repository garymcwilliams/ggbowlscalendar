"""
test
"""
from datetime import datetime as dt
from datetime import date as dt_date
from ggbowlscalendar.league_results_manager import (
    LeagueResultsManager,
    TBD_DATA,
    TBD_DISPLAY
)

DATE1 = '2023-04-22'
DATE2 = '2023-04-30'


def combine_date_time_str(date: str, time: str):
    """combine date and time"""
    calc_date = dt.strptime(date, '%Y-%m-%d').date()
    return combine_date_time(calc_date, time)


def combine_date_time(date: dt_date, time: str):
    """combine date and time"""
    calc_time = dt.strptime(time, '%H:%M').time()
    return dt.combine(date, calc_time)


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
                     'date': dt.strptime(DATE1, '%Y-%m-%d'),
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
                     'date': dt.strptime(DATE1, '%Y-%m-%d'),
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
        assert match.match_date_time() == combine_date_time_str(DATE1, "14:00")

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
                     'date': dt.strptime(DATE1, '%Y-%m-%d'),
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
        assert match.match_date_time() == combine_date_time_str(DATE1, "14:00")

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
                     'date': dt.strptime(DATE1, '%Y-%m-%d'),
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
                     'date': dt.strptime(DATE1, '%Y-%m-%d'),
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
        assert match.match_date_time() == combine_date_time_str(DATE1, time)

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
                     'date': dt.strptime(DATE1, '%Y-%m-%d'),
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
        assert match.match_date_time() == combine_date_time_str(DATE1, time)

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
                     'date': dt.strptime(DATE1, '%Y-%m-%d'),
                     'newdate': dt.strptime(DATE2, '%Y-%m-%d'),
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
        assert match.match_date_time() == combine_date_time_str(DATE2, time)

    """
    Disabled for now, we currently no longer support a "no new date time" scenario.
    """
    # def test_match_nonewdatetime(self):
    #     """
    #     test if we have no date for a game
    #     """

    #     time = "18:30"
    #     match_dict = {
    #         'me': 'FALLSA',
    #         'start_time': '14:00',
    #         'day': 'Sat',
    #         'duration': 3,
    #         'matches':
    #             [
    #                 {'away': 'CLIFT',
    #                  'date': dt.strptime(DATE1, '%Y-%m-%d'),
    #                  'newdate': TBD_DATA,
    #                  'newtime': time,
    #                  'our_score': 0.0,
    #                  'opp_score': 0.0,
    #                  },
    #             ]
    #     }

    #     results_manager = LeagueResultsManager.from_dict(match_dict)
    #     match = results_manager.results[0]
    #     assert match.match_date_time() is None
    #     assert match.is_away()
    #     assert match.not_played_yet() is True
    #     assert match.result == ' '
    #     assert match.label == TBD_DISPLAY
    #     assert match.notes() == TBD_DISPLAY
    #     assert match.format_our_score() is None
    #     assert match.format_opp_score() is None

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
                     'date': dt.strptime(DATE1, '%Y-%m-%d'),
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
        assert match.match_date_time() == combine_date_time_str(DATE1, "14:00")

    def test_match_neutral_vanue(self):
        """
        tests a neutral venue location
        """

        match_dict = {
            'me': 'FALLSA',
            'start_time': '14:00',
            'day': 'Sat',
            'duration': 3,
            'matches':
                [
                    {'home': 'CLIFT',
                     'date': dt.strptime(DATE1, '%Y-%m-%d'),
                     'location': 'NEUTR',
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
        assert match.match_date_time() == combine_date_time_str(DATE1, "14:00")
