"""
Tests for printer.py and utils.py.
"""

from __future__ import annotations

import os
import tempfile
from datetime import date, time
from pathlib import Path
from unittest.mock import patch

import pytest

from conftest import make_match, make_league, _FakeConsole, _FakeTable
from ggbowlscalendar.models import TBD_DISPLAY, VENUE_AWAY, VENUE_HOME
from ggbowlscalendar.printer import (
    _display_opp_name,
    _format_date,
    _row_values,
    print_results,
)


# ===========================================================================
# _display_opp_name
# ===========================================================================

class TestDisplayOppName:

    def test_normal_name_returned_unchanged(self):
        assert _display_opp_name(make_match(), "Opponents FC") == "Opponents FC"

    def test_unknown_team_wrapped_in_red_markup(self):
        result = _display_opp_name(make_match(), "***UNKNOWN***")
        assert "[red]" in result
        assert "***UNKNOWN***" in result

    def test_club_comp_uses_opp_id(self):
        m = make_match(opp_id="ClubKnockout")
        assert _display_opp_name(m, "Club Championship") == "ClubKnockout"

    def test_sub_team_appended(self):
        assert _display_opp_name(make_match(sub_team="B"), "Opponents FC") == "Opponents FC B"

    def test_no_none_suffix_when_sub_team_absent(self):
        assert "None" not in _display_opp_name(make_match(), "Opponents FC")


# ===========================================================================
# _format_date
# ===========================================================================

class TestFormatDate:

    DEFAULT_DAY = "Tue"
    DEFAULT_TIME = time(18, 0)

    def _fmt(self, match, day=None, t=None):
        return _format_date(match, day or self.DEFAULT_DAY, t or self.DEFAULT_TIME)

    def test_tbd_returns_tbd_display(self):
        assert self._fmt(make_match(rescheduled_date=TBD)) == TBD_DISPLAY

    def test_default_day_match_has_no_day_prefix(self):
        # date(2024, 5, 14) is a Tuesday — same as DEFAULT_DAY
        result = self._fmt(make_match(match_date=date(2024, 5, 14), start_time=time(18, 0)))
        assert "14-May" in result
        assert "Tue" not in result

    def test_non_default_day_shows_weekday_prefix(self):
        # date(2024, 5, 16) is a Thursday
        result = self._fmt(make_match(match_date=date(2024, 5, 16)))
        assert "Thu" in result
        assert "16-May" in result

    def test_default_time_not_printed(self):
        # start_time matches DEFAULT_TIME — time should be suppressed
        result = self._fmt(make_match(match_date=date(2024, 5, 14), start_time=time(18, 0)))
        assert "18:00" not in result

    def test_non_default_time_printed(self):
        # rescheduled to 14:00 which differs from default 18:00
        m = make_match(match_date=date(2024, 5, 14), rescheduled_time=time(14, 0))
        result = self._fmt(m)
        assert "14:00" in result

    def test_rescheduled_date_and_different_time_both_shown(self):
        m = make_match(
            match_date=date(2024, 5, 14),
            rescheduled_date=date(2024, 5, 18),  # a Saturday
            rescheduled_time=time(14, 0),
        )
        result = self._fmt(m)
        assert "18-May" in result
        assert "14:00" in result

    def test_rescheduled_date_same_time_no_time_suffix(self):
        # Rescheduled to a different date but same kick-off time
        m = make_match(
            match_date=date(2024, 5, 14),
            rescheduled_date=date(2024, 5, 18),
            rescheduled_time=time(18, 0),
        )
        result = self._fmt(m)
        assert "18-May" in result
        assert "18:00" not in result


# ===========================================================================
# _row_values
# ===========================================================================

class TestRowValues:

    @pytest.fixture
    def ctx(self, registry):
        return make_league(), registry

    def test_row_has_seven_columns(self, registry):
        row = _row_values(make_match(), make_league(), registry)
        assert len(row) == 7

    @pytest.mark.parametrize("our, their, expected_code", [
        (None, None, " "),
        (5,    2,    "W"),
        (1,    4,    "L"),
        (3,    3,    "D"),
    ])
    def test_result_column(self, registry, our, their, expected_code):
        row = _row_values(make_match(our_score=our, opp_score=their), make_league(), registry)
        assert expected_code in row[0]

    @pytest.mark.parametrize("venue, colour", [
        (VENUE_HOME, "[red]"),
        (VENUE_AWAY, "[blue]"),
    ])
    def test_venue_colour_markup(self, registry, venue, colour):
        row = _row_values(make_match(venue=venue), make_league(), registry)
        assert colour in row[1]

    def test_score_columns_empty_when_unplayed(self, registry):
        row = _row_values(make_match(), make_league(), registry)
        assert row[2] == ""
        assert row[3] == ""

    def test_score_columns_filled_when_played(self, registry):
        row = _row_values(make_match(our_score=4, opp_score=1), make_league(), registry)
        assert row[2] == "4"
        assert row[3] == "1"

    def test_opponent_name_column(self, registry):
        row = _row_values(make_match(opp_id="OPP1"), make_league(), registry)
        assert row[4] == "Opponents FC"

    def test_notes_column(self, registry):
        row = _row_values(make_match(label="Cup Final"), make_league(), registry)
        assert row[6] == "Cup Final"


# ===========================================================================
# print_results
# ===========================================================================

class TestPrintResults:

    def test_empty_league_prints_no_results_message(self, registry):
        console = _FakeConsole()
        with patch("ggbowlscalendar.printer.Console", return_value=console):
            print_results(make_league([]), registry)
        assert any("No results" in str(p) for p in console.printed)

    def test_non_empty_league_prints_table(self, registry):
        console, table = _FakeConsole(), _FakeTable()
        with patch("ggbowlscalendar.printer.Console", return_value=console), \
             patch("ggbowlscalendar.printer.Table", return_value=table):
            print_results(make_league([make_match()]), registry)
        assert table in console.printed

    def test_table_columns(self, registry):
        table = _FakeTable()
        with patch("ggbowlscalendar.printer.Console", return_value=_FakeConsole()), \
             patch("ggbowlscalendar.printer.Table", return_value=table):
            print_results(make_league([make_match()]), registry)
        assert table.columns == ["R", "Venue", "Us", "Opp", "Opponent", "Date", "Note"]

    @pytest.mark.parametrize("count", [1, 2, 3])
    def test_row_count_matches_match_count(self, registry, count):
        matches = [make_match(match_date=date(2024, 5, 14 + i)) for i in range(count)]
        table = _FakeTable()
        with patch("ggbowlscalendar.printer.Console", return_value=_FakeConsole()), \
             patch("ggbowlscalendar.printer.Table", return_value=table):
            print_results(make_league(matches), registry)
        assert len(table.rows) == count


# ===========================================================================
# utils
# ===========================================================================

class TestGetOutputDir:

    def test_raises_when_ical_output_not_set(self):
        from ggbowlscalendar import utils
        clean_env = {k: v for k, v in os.environ.items() if k != "ICAL_OUTPUT"}
        with patch.dict("os.environ", clean_env, clear=True):
            with pytest.raises(EnvironmentError):
                utils.get_output_dir()

    def test_returns_path_under_ical_output(self, tmp_path):
        from ggbowlscalendar import utils
        with patch.dict("os.environ", {"ICAL_OUTPUT": str(tmp_path)}):
            result = utils.get_output_dir()
        assert str(result).startswith(str(tmp_path))

    def test_creates_apps_icalendar_subdirectory(self, tmp_path):
        from ggbowlscalendar import utils
        with patch.dict("os.environ", {"ICAL_OUTPUT": str(tmp_path)}):
            result = utils.get_output_dir()
        assert result.is_dir()
        assert result == tmp_path / "Apps" / "icalendar"


class TestFindDataFile:

    def test_raises_when_file_missing(self):
        from ggbowlscalendar import utils
        with patch("ggbowlscalendar.utils.env") as mock_env:
            mock_env.read_envfile = lambda: None
            mock_env.str = lambda k: "/nonexistent"
            with pytest.raises(FileNotFoundError):
                utils.find_data_file("missing.yml")

    def test_returns_path_when_file_exists(self, tmp_path):
        from ggbowlscalendar import utils
        target = tmp_path / "teams.yml"
        target.touch()
        with patch("ggbowlscalendar.utils.env") as mock_env:
            mock_env.read_envfile = lambda: None
            mock_env.str = lambda k: str(tmp_path)
            assert utils.find_data_file("teams.yml") == target

    def test_subfolder_path_resolved(self, tmp_path):
        from ggbowlscalendar import utils
        sub = tmp_path / "myclub"
        sub.mkdir()
        target = sub / "myclub_games_2024.yml"
        target.touch()
        with patch("ggbowlscalendar.utils.env") as mock_env:
            mock_env.read_envfile = lambda: None
            mock_env.str = lambda k: str(tmp_path)
            assert utils.find_data_file("myclub_games_2024.yml", subfolder="myclub") == target


class TestLoadYaml:

    def test_parses_yaml_file(self, tmp_path):
        from ggbowlscalendar import utils
        f = tmp_path / "data.yml"
        f.write_text("key: value\nnumber: 42\n")
        result = utils.load_yaml(f)
        assert result["key"] == "value"
        assert result["number"] == 42


class TestWriteIcalFile:

    def test_writes_content_to_correct_path(self, tmp_path):
        from ggbowlscalendar import utils
        content = b"BEGIN:VCALENDAR\nEND:VCALENDAR"
        with patch.dict("os.environ", {"ICAL_OUTPUT": str(tmp_path)}):
            utils.write_ical_file("test.ics", content)
        written = tmp_path / "Apps" / "icalendar" / "test.ics"
        assert written.exists()
        assert written.read_bytes() == content
