"""
test
"""
import datetime

import pytest
from ggbowlscalendar.results_table_ical import ResultsTableIcal
from ggbowlscalendar.league_results_manager import (
    LeagueResultsManager,
    TBD_DATA
)
from ggbowlscalendar.team_manager import TeamManager


DATE_230422 = datetime.datetime.strptime("2023-04-22", '%Y-%m-%d')
DATE_230430 = datetime.datetime.strptime("2023-04-30", '%Y-%m-%d')
UTCNOW = datetime.datetime.now(datetime.timezone.utc)

FALLSA = "FALLSA"
FALLSA_NAME = "Falls A"
FALLSA_LOC = f"{FALLSA_NAME} location"
CLIFT = "CLIFT"
CLIFT_NAME = "Cliftonville"
CLIFT_NAME_BRACES = f"({CLIFT_NAME})"
CLIFT_LOC = f"{CLIFT_NAME} location"
NEUTR = "NEUTR"
NEUTR_NAME = "Neutral"
NEUTR_LOC = f"{NEUTR_NAME} location"

TEAM_DICT = {
    FALLSA: {'name': FALLSA_NAME, 'location': FALLSA_LOC},
    CLIFT: {'name': CLIFT_NAME, 'location': CLIFT_LOC},
    NEUTR: {'name': NEUTR_NAME, 'location': NEUTR_LOC},
}

testdata = [
    ("home", 6, 1, "W"),
    ("home", 1, 6, "L"),
    ("home", 3, 3, "D"),
    ("home", 0, 0, " "),
    ("away", 6, 1, "W"),
    ("away", 1, 6, "L"),
    ("away", 3, 3, "D"),
    ("away", 0, 0, " "),
]


@pytest.mark.parametrize("venue,our_score,opp_score,expected_result", testdata)
def test_result_event(venue: str,
                      our_score: int,
                      opp_score: int,
                      expected_result: str):
    """
    test all basic methods for results as ical events.

    NOTE: ALSO check that TBD games don't get included in ical
    """

    match_dict = {
        'me': FALLSA,
        'start_time': '14:00',
        'day': 'Sat',
        'duration': 3,
        'matches':
            [
                {
                    venue: CLIFT,
                    'label': 'Irish Cup',
                    'date': DATE_230422,
                    'our_score': our_score,
                    'opp_score': opp_score,
                },
                {
                    'away': 'CLIFT',
                    'date': DATE_230430,
                    'newdate': TBD_DATA,
                    'our_score': 0,
                    'opp_score': 0,
                },
            ]
    }

    results_manager = LeagueResultsManager.from_dict(match_dict)

    team_manager = TeamManager.from_dict(TEAM_DICT)

    if venue == 'home':
        home_name = FALLSA_NAME
        away_name = CLIFT_NAME_BRACES
        location = FALLSA_LOC
    else:
        home_name = CLIFT_NAME_BRACES
        away_name = FALLSA_NAME
        location = CLIFT_LOC
    match_names = f"{home_name} v {away_name}"

    if our_score == 0 and opp_score == 0:
        score_display = ""
        description = f'{venue} {CLIFT_NAME_BRACES}'
    else:
        score_display = f"{expected_result} ({our_score} - {opp_score}) "
        description = f'{expected_result} {venue} {CLIFT_NAME_BRACES}'

    ical_generator = ResultsTableIcal(results_manager, team_manager)
    for result in results_manager.results:
        if result.newdate is None or result.newdate != TBD_DATA:
            event = ical_generator._create_event(result,
                                                 UTCNOW)
            assert event.get('UID') == \
                f'{FALLSA}-202304221400IrishCup@mc-williams.co.uk'
            assert event.get('LOCATION') == location
            expected_summary = (
                                f"{match_names} "
                                f"{score_display}"
                                "Irish Cup"
                                )
            assert event.get('SUMMARY') == expected_summary
            assert event.get('DESCRIPTION') == description

    dtstamp = UTCNOW.strftime('%Y%m%dT%H%M%SZ')
    ical_content = (
                    "BEGIN:VCALENDAR\r\n"
                    "VERSION:2.0\r\n"
                    "PRODID:-//Bowling Calendar//mc-williams.co.uk//\r\n"
                    "CALSCALE:GREGORIAN\r\n"
                    "X-WR-TIMEZONE:Europe/London\r\n"
                    "BEGIN:VEVENT\r\n"
                    f"SUMMARY:{expected_summary}\r\n"
                    "DTSTART;VALUE=DATE-TIME:20230422T135000\r\n"
                    "DTEND;VALUE=DATE-TIME:20230422T170000\r\n"
                    f"DTSTAMP;VALUE=DATE-TIME:{dtstamp}\r\n"
                    "UID:FALLSA-202304221400IrishCup@mc-williams.co.uk\r\n"
                    f"DESCRIPTION:{description}\r\n"
                    f"LOCATION:{location}\r\n"
                    "PRIORITY:5\r\n"
                    "BEGIN:VALARM\r\n"
                    "ACTION:DISPLAY\r\n"
                    "DESCRIPTION:Reminder\r\n"
                    "TRIGGER:-PT1H\r\n"
                    "END:VALARM\r\n"
                    "END:VEVENT\r\n"
                    "END:VCALENDAR\r\n"
                    )

    ical_generator.generate_ical()
    ical_bytes = ical_generator.cal.to_ical()
    assert ical_bytes == ical_content.encode()


def test_result_neutral():
    """
    test neutral vanue
    """

    match_dict = {
        'me': FALLSA,
        'start_time': '14:00',
        'day': 'Sat',
        'duration': 3,
        'matches':
            [
                {
                    'away': CLIFT,
                    'location': 'NEUTR',
                    'date': DATE_230422,
                    'newdate': DATE_230430,
                    'newtime': '18:30',
                    'our_score': 6,
                    'opp_score': 1,
                },
            ]
    }

    results_manager = LeagueResultsManager.from_dict(match_dict)

    team_manager = TeamManager.from_dict(TEAM_DICT)

    away_name = FALLSA_NAME
    home_name = CLIFT_NAME_BRACES
    location = NEUTR_LOC
    match_names = f"{home_name} v {away_name}"

    score_display = "W (6 - 1)"
    description = f'W neutral {CLIFT_NAME_BRACES}'

    ical_generator = ResultsTableIcal(results_manager, team_manager)
    for result in results_manager.results:
        if result.newdate is None or result.newdate != TBD_DATA:
            event = ical_generator._create_event(result,
                                                 UTCNOW)
            assert event.get('UID') == \
                f'{FALLSA}-202304221400@mc-williams.co.uk'
            assert event.get('LOCATION') == location
            expected_summary = (
                                f"{match_names} "
                                f"{score_display}"
                                )
            assert event.get('SUMMARY') == expected_summary
            assert event.get('DESCRIPTION') == description

    dtstamp = UTCNOW.strftime('%Y%m%dT%H%M%SZ')
    ical_content = (
                    "BEGIN:VCALENDAR\r\n"
                    "VERSION:2.0\r\n"
                    "PRODID:-//Bowling Calendar//mc-williams.co.uk//\r\n"
                    "CALSCALE:GREGORIAN\r\n"
                    "X-WR-TIMEZONE:Europe/London\r\n"
                    "BEGIN:VEVENT\r\n"
                    f"SUMMARY:{expected_summary}\r\n"
                    "DTSTART;VALUE=DATE-TIME:20230430T182000\r\n"
                    "DTEND;VALUE=DATE-TIME:20230430T213000\r\n"
                    f"DTSTAMP;VALUE=DATE-TIME:{dtstamp}\r\n"
                    "UID:FALLSA-202304221400@mc-williams.co.uk\r\n"
                    f"DESCRIPTION:{description}\r\n"
                    f"LOCATION:{location}\r\n"
                    "PRIORITY:5\r\n"
                    "BEGIN:VALARM\r\n"
                    "ACTION:DISPLAY\r\n"
                    "DESCRIPTION:Reminder\r\n"
                    "TRIGGER:-PT1H\r\n"
                    "END:VALARM\r\n"
                    "END:VEVENT\r\n"
                    "BEGIN:VEVENT\r\n"
                    f"SUMMARY:{match_names}\r\n"
                    "DTSTART;VALUE=DATE-TIME:20230430T173000\r\n"
                    "DTEND;VALUE=DATE-TIME:20230430T174000\r\n"
                    f"DTSTAMP;VALUE=DATE-TIME:{dtstamp}\r\n"
                    "UID:DEP-FALLSA-202304221400@mc-williams.co.uk\r\n"
                    f"DESCRIPTION:{description}\r\n"
                    f"LOCATION:{location}\r\n"
                    "PRIORITY:5\r\n"
                    "BEGIN:VALARM\r\n"
                    "ACTION:DISPLAY\r\n"
                    "DESCRIPTION:Reminder\r\n"
                    "TRIGGER:-PT1H\r\n"
                    "END:VALARM\r\n"
                    "END:VEVENT\r\n"
                    "END:VCALENDAR\r\n"
                    )

    ical_generator.generate_ical()
    ical_bytes = ical_generator.cal.to_ical()
    with open("gary.txt", "wb") as binary_file:
        # Write bytes to file
        binary_file.write(ical_bytes)
    assert ical_bytes == ical_content.encode()


def test_result_newdate():
    """
    test newdate for results as ical events.
    """

    match_dict = {
        'me': FALLSA,
        'start_time': '14:00',
        'day': 'Sat',
        'duration': 3,
        'matches':
            [
                {
                    'home': CLIFT,
                    'date': DATE_230422,
                    'newdate': DATE_230430,
                    'newtime': '18:30',
                    'our_score': 6,
                    'opp_score': 1,
                },
            ]
    }

    results_manager = LeagueResultsManager.from_dict(match_dict)

    team_manager = TeamManager.from_dict(TEAM_DICT)

    home_name = FALLSA_NAME
    away_name = CLIFT_NAME_BRACES
    location = FALLSA_LOC
    match_names = f"{home_name} v {away_name}"

    score_display = "W (6 - 1)"
    description = f'W home {CLIFT_NAME_BRACES}'

    ical_generator = ResultsTableIcal(results_manager, team_manager)
    for result in results_manager.results:
        if result.newdate is None or result.newdate != TBD_DATA:
            event = ical_generator._create_event(result,
                                                 UTCNOW)
            assert event.get('UID') == \
                f'{FALLSA}-202304221400@mc-williams.co.uk'
            assert event.get('LOCATION') == location
            expected_summary = (
                                f"{match_names} "
                                f"{score_display}"
                                )
            assert event.get('SUMMARY') == expected_summary
            assert event.get('DESCRIPTION') == description

    dtstamp = UTCNOW.strftime('%Y%m%dT%H%M%SZ')
    ical_content = (
                    "BEGIN:VCALENDAR\r\n"
                    "VERSION:2.0\r\n"
                    "PRODID:-//Bowling Calendar//mc-williams.co.uk//\r\n"
                    "CALSCALE:GREGORIAN\r\n"
                    "X-WR-TIMEZONE:Europe/London\r\n"
                    "BEGIN:VEVENT\r\n"
                    f"SUMMARY:{expected_summary}\r\n"
                    "DTSTART;VALUE=DATE-TIME:20230430T182000\r\n"
                    "DTEND;VALUE=DATE-TIME:20230430T213000\r\n"
                    f"DTSTAMP;VALUE=DATE-TIME:{dtstamp}\r\n"
                    "UID:FALLSA-202304221400@mc-williams.co.uk\r\n"
                    f"DESCRIPTION:{description}\r\n"
                    f"LOCATION:{location}\r\n"
                    "PRIORITY:5\r\n"
                    "BEGIN:VALARM\r\n"
                    "ACTION:DISPLAY\r\n"
                    "DESCRIPTION:Reminder\r\n"
                    "TRIGGER:-PT1H\r\n"
                    "END:VALARM\r\n"
                    "END:VEVENT\r\n"
                    "END:VCALENDAR\r\n"
                    )

    ical_generator.generate_ical()
    ical_bytes = ical_generator.cal.to_ical()
    assert ical_bytes == ical_content.encode()


def test_no_results():
    """
    tests for no results provided
    """

    match_dict = {
        'me': 'FALLSA',
        'start_time': '14:00',
        'day': 'Sat',
        'duration': 3,
        'matches':
            [
            ]
    }

    results_manager = LeagueResultsManager.from_dict(match_dict)

    team_manager = TeamManager.from_dict(TEAM_DICT)

    ical_generator = ResultsTableIcal(results_manager, team_manager)
    ical_generator.generate_ical()
