from rich.console import Console
from rich.table import Table

from .league_results_manager import TBD_DISPLAY, LeagueResult, LeagueResultsManager
from .team_manager import TeamData, TeamManager

DISPLAY_WON = "[green]W :heavy_check_mark:[/]"
DISPLAY_LOST = "[red]L[/]"
DISPLAY_DREW = "D"
DISPLAY_NOT_PLAYED = " "
DISPLAY_RESULTS = {
    "W": DISPLAY_WON,
    "L": DISPLAY_LOST,
    "D": DISPLAY_DREW,
    " ": DISPLAY_NOT_PLAYED,
}

COLOURS = {"home": "red", "away": "blue"}


class ResultsTablePrinter:
    """Print results in a Table"""

    def __init__(
        self, results_manager: LeagueResultsManager, team_manager: TeamManager
    ) -> None:
        """
        Setup data for printing the results

        Args:
            results_manager (LeagueResultsManager): The manager containing the
            results.
            team_manager (TeamManager): The team manager containing the team
            details.
        """
        self.results_manager = results_manager
        self.team_manager = team_manager
        self.default_day = results_manager.default_day
        self.console = Console()
        self.table = Table(show_header=True, header_style="bold magenta")

    def print(self) -> None:
        """Display the league results."""

        self._print_table_header()

        for result in self.results_manager.results:
            opp_team_details = self.team_manager.get_team_details(result.opp_id)

            self.add_match_to_table(result, opp_team_details)

        self.print_match_table()

        if not self.results_manager.results:
            self.console.print("No results found.")

    def _print_table_header(self) -> None:
        """print the header row"""
        self.table.add_column("R")
        self.table.add_column("venue")
        self.table.add_column("Us")
        self.table.add_column("Op")
        self.table.add_column("opp")
        self.table.add_column("date")
        self.table.add_column("note")

    def _not_normal_day(self, result: LeagueResult) -> bool:
        """
        work out if this match is being played on the regular/normal day for
        this team
        """
        match_date_time = result.match_date_time()
        return bool(match_date_time and match_date_time.strftime("%a") != self.default_day)

    def add_match_to_table(self, result: LeagueResult, opp: TeamData) -> None:
        """format this result as a line in the table"""

        opp_name = opp.name
        if opp_name.startswith("***"):
            opp_name = f"[red]{opp_name}[/red]"
        if opp_name.startswith("Club"):
            opp_name = result.opp_id
        if result.sub_team:
            opp_name = f"{opp_name} {result.sub_team}"

        date_display = TBD_DISPLAY
        if result.match_date_time():
            # only show date if there is one in place, allows for as-yet
            # unscheduled games to be processed
            day_pattern = "   "
            # only show day if it's not the 'normal' one
            if self._not_normal_day(result):
                day_pattern = "%a"
            date_pattern = f"{day_pattern} %d-%b %H:%M"
            date_display = result.match_date_time().strftime(date_pattern)

        result_display = DISPLAY_RESULTS[result.result]

        venue = f"[{COLOURS[result.venue]}]{result.venue}[/]"
        self.table.add_row(
            result_display,
            venue,
            result.format_our_score(),
            result.format_opp_score(),
            opp_name,
            date_display,
            result.notes(),
        )

    def print_match_table(self) -> None:
        """Print the table once it has been generated"""
        self.console.print(self.table)
