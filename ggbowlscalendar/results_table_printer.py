from rich.console import Console
from rich.table import Table

from .league_results_manager import LeagueResultsManager, LeagueResult
from .team_manager import TeamManager, Team


class ResultsTablePrinter:
    """Print results in a Table"""

    def __init__(self,
                 results_manager: LeagueResultsManager,
                 team_manager: TeamManager) -> None:
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
        """ Display the league results.  """

        self._print_table_header()

        for result in self.results_manager.results:
            opp_team_details = self.team_manager.get_team_details(
                result.opp_id
            )

            self.add_match_to_table(result, opp_team_details)

        self.print_match_table()

        if not self.results_manager.results:
            print("No results found.")

    def _print_table_header(self) -> None:
        """print the header row"""
        self.table.add_column("R")
        self.table.add_column("venue")
        self.table.add_column("Us")
        self.table.add_column("Op")
        self.table.add_column("opp")
        self.table.add_column("date")
        self.table.add_column("note")

    def add_match_to_table(self,
                           result: LeagueResult,
                           opp: Team) -> None:
        """format this result as a line in the table"""

        opp_name = (
            f"{opp['name']} {result.sub_team}" if result.sub_team
            else opp['name']
        )

        day_pattern = (
            "%a" if result.match_date_time().strftime('%a') != self.default_day
            else "   "
        )
        date_pattern = f'{day_pattern} %d-%b %H:%M'
        result_display = (
            f"[green]{result.result} :heavy_check_mark:"
            if result.result == "W"
            else f"[red]{result.result}" if result.result == "L"
            else result.result
        )
        colours = {'home': 'red', 'away': 'blue'}
        venue = f"[{colours[result.venue]}]{result.venue}[/]"
        self.table.add_row(
            result_display,
            venue,
            result.format_our_score(),
            result.format_opp_score(),
            opp_name,
            result.match_date_time().strftime(date_pattern),
            result.notes(),
        )

    def print_match_table(self) -> None:
        """Print the table once it has been generated"""
        self.console.print(self.table)
