from .context import Match

import pytest

FALLS_A = "Falls A"
OLD_BLEACH_A = "Old Bleach A"


class TestMatch:
    ###########################################################################
    #  H O M E
    ###########################################################################
    @pytest.fixture(scope="class")
    def home_match(self) -> Match:
        return Match(
            myclub="FALLSA",
            home_team_id="FALLSA",
            home_team_name=FALLS_A,
            home_score=6,
            away_team_id="OLDLA",
            away_team_name=OLD_BLEACH_A,
            away_score=1,
            date="2018-06-05",
            time="18:30",
            location="location",
            duration=3,
        )

    def test_home_match_description(self, home_match):
        assert (
            home_match.description()
            == "W Falls A (6) v (1) Old Bleach A 2018-06-05@18:30"
        )

    def test_home_match_print_description(self, home_match):
        assert (
            home_match.print_description()
            == "W Falls A         (  6) v (  1) Old Bleach A    "
            "2018-06-05@18:30"
        )

    def test_home_match_id(self, home_match):
        assert home_match.id() == "FALLSA-201806051830@mc-williams.co.uk"

    ###########################################################################
    #  H O M E   A W A Y   N O T   K N O W N
    ###########################################################################
    @pytest.fixture(scope="class")
    def home_awaynotknown(self) -> Match:
        return Match(
            myclub="FALLSA",
            home_team_id="FALLSA",
            home_team_name=FALLS_A,
            home_score=6,
            away_team_id="OLDLA",
            away_team_name=OLD_BLEACH_A,
            away_score=1,
            date="2018-06-05",
            time="18:30",
            location="location",
            duration=3,
            warning="****",
        )

    def test_home_awaynotknown_print_description(self, home_awaynotknown):
        assert (
            home_awaynotknown.print_description()
            == "W Falls A         (  6) v (  1) Old Bleach A    "
            "2018-06-05@18:30 ****"
        )

    ###########################################################################
    # H O M E   N E W   D A T E
    ###########################################################################
    @pytest.fixture(scope="class")
    def home_match_newdate(self) -> Match:
        return Match(
            myclub="FALLSA",
            home_team_id="FALLSA",
            home_team_name=FALLS_A,
            home_score=6,
            away_team_id="OLDLA",
            away_team_name=OLD_BLEACH_A,
            away_score=1,
            date="2018-06-05",
            time="18:30",
            location="location",
            duration=3,
            new_date="2018-06-06",
        )

    def test_home_match_newdate_description(self, home_match_newdate):
        assert (
            home_match_newdate.description()
            == "W Falls A (6) v (1) Old Bleach A 2018-06-06@18:30"
        )

    def test_home_match_newdate_print_description(self, home_match_newdate):
        assert (
            home_match_newdate.print_description()
            == "W Falls A         (  6) v (  1) Old Bleach A    "
            "2018-06-06@18:30"
        )

    def test_home_match_newdate_id(self, home_match_newdate):
        assert home_match_newdate.id() == 'FALLSA-201806051830@' \
            'mc-williams.co.uk'

    ###########################################################################
    # H O M E   N E W   D A T E   A N D   T I M E
    ###########################################################################
    @pytest.fixture(scope="class")
    def home_newdatetime(self) -> Match:
        return Match(
            myclub="FALLSA",
            home_team_id="FALLSA",
            home_team_name=FALLS_A,
            home_score=6,
            away_team_id="OLDLA",
            away_team_name=OLD_BLEACH_A,
            away_score=1,
            date="2018-06-05",
            time="18:30",
            location="location",
            duration=3,
            new_date="2018-06-06",
            new_time="14:00",
        )

    def test_home_newdatetime_description(self, home_newdatetime):
        assert (
            home_newdatetime.description()
            == "W Falls A (6) v (1) Old Bleach A 2018-06-06@14:00"
        )

    def test_home_newdatetime_print_description(self, home_newdatetime):
        assert (
            home_newdatetime.print_description()
            == "W Falls A         (  6) v (  1) Old Bleach A    "
            "2018-06-06@14:00"
        )

    def test_home_match_newdatetime_id(self, home_newdatetime):
        assert home_newdatetime.id() == "FALLSA-201806051830@" \
            "mc-williams.co.uk"

    ###########################################################################
    # H O M E   N E W   D A T E   N O T   K N O W N
    ###########################################################################
    @pytest.fixture(scope="class")
    def home_newdateunknwon(self) -> Match:
        return Match(
            myclub="FALLSA",
            home_team_id="FALLSA",
            home_team_name=FALLS_A,
            home_score=6,
            away_team_id="OLDLA",
            away_team_name=OLD_BLEACH_A,
            away_score=1,
            date="2018-06-05",
            time="18:30",
            location="location",
            duration=3,
            new_date="",
        )

    def test_home_newdateunknwon_description(self, home_newdateunknwon):
        assert (
            home_newdateunknwon.description()
            == "W Falls A (6) v (1) Old Bleach A 2018-06-05@18:30 "
            "****-TBD-****"
        )

    def test_home_newdateunknwon_print_description(self, home_newdateunknwon):
        assert (
            home_newdateunknwon.print_description()
            == "W Falls A         (  6) v (  1) Old Bleach A    "
            "2018-06-05@18:30 ****-TBD-****"
        )

    def test_home_newdateunknwon_id(self, home_newdateunknwon):
        assert home_newdateunknwon.id() == "FALLSA-201806051830@" \
            "mc-williams.co.uk"

    ###########################################################################
    #  A W A Y
    ###########################################################################
    @pytest.fixture(scope="class")
    def away_match(self) -> Match:
        return Match(
            myclub="FALLSA",
            home_team_id="DUNBA",
            home_team_name="Dunbarton",
            home_score=7,
            away_team_id="FALLSA",
            away_team_name=FALLS_A,
            away_score=0,
            date="2018-05-29",
            time="14:00",
            location="location",
            duration=3,
        )

    def test_at_away_description(self, away_match):
        assert (
            away_match.description()
            == "L Dunbarton (7) v (0) Falls A 2018-05-29@14:00"
        )

    def test_at_away_id(self, away_match):
        assert away_match.id() == "FALLSA-201805291400@mc-williams.co.uk"

    def test_at_away_print_description(self, away_match):
        assert (
            away_match.print_description()
            == "L Dunbarton       (  7) v (  0) Falls A         "
            "2018-05-29@14:00"
        )

    ###########################################################################
    #  C U P
    ###########################################################################
    @pytest.fixture(scope="class")
    def cup_home_match(self) -> Match:
        return Match(
            myclub="FALLSA",
            home_team_id="FALLSA",
            home_team_name=FALLS_A,
            home_score=96,
            away_team_id="Limavady",
            away_team_name="Limavady",
            away_score=71,
            date="2018-06-02",
            time="14:00",
            location="location",
            warning="****",
            duration=3,
            label="Irish Cup",
        )

    def test_cup_home_match_description(self, cup_home_match):
        assert (
            cup_home_match.description()
            == "W Falls A (96) v (71) Limavady 2018-06-02@14:00 Irish Cup"
        )

    def test_cup_home_match_print_description(self, cup_home_match):
        assert (
            cup_home_match.print_description()
            == "W Falls A         ( 96) v ( 71) Limavady        "
            "2018-06-02@14:00 Irish Cup ****"
        )

    ###########################################################################
    #  N O T   Y E T   P L A Y E D
    ###########################################################################
    @pytest.fixture(scope="class")
    def notyet_home_match(self) -> Match:
        return Match(
            myclub="FALLSA",
            home_team_id="FALLSA",
            home_team_name=FALLS_A,
            home_score=0,
            away_team_id="Limavady",
            away_team_name="Limavady",
            away_score=0,
            date="2018-06-02",
            time="14:00",
            location="location",
            warning="",
            duration=3
        )

    def test_notyet_home_match_description(self, notyet_home_match):
        assert (
            notyet_home_match.description()
            == ". Falls A (0) v (0) Limavady 2018-06-02@14:00"
        )

    def test_notyet_home_match_print_description(self, notyet_home_match):
        assert (
            notyet_home_match.print_description()
            == ". Falls A         (  0) v (  0) Limavady        "
            "2018-06-02@14:00"
        )
