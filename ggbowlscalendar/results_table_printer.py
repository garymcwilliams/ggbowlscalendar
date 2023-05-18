from rich.console import Console
from rich.table import Table

from league_results_manager import LeagueResultsManager, LeagueResult
from team_manager import TeamManager, Team


class ResultsTablePrinter:
    """Print results in a Table"""

    def __init__(self, results_manager: LeagueResultsManager, team_manager: TeamManager) -> None:
        self.results_manager = results_manager
        self.team_manager = team_manager
        self.console = Console()
        self.table = Table(show_header=True, header_style="bold magenta")

    def print(self) -> None:
        """
        Display the league results.

        Args:
            results_manager (LeagueResultsManager): The manager containing the results.
            team_manager (TeamManager): The team manager containing the team details.
        """

        self._print_table_header()

        for result in self.results_manager.results:
            my_team_details = self.team_manager.get_team_details(self.results_manager.myTeam)
            opp_team_details = self.team_manager.get_team_details(result.opp_id)

            location = my_team_details.get("location") if result.venue == "home" else opp_team_details.get("location")

            self.add_match_to_table(result, my_team_details, opp_team_details)

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

    def add_match_to_table(self, result: LeagueResult, me: Team, opp: Team) -> None:
        """format this result as a line in the table"""

        opp_name = (
            f"{opp['name']} {result.sub_team}" if result.sub_team
            else opp['name']
        )

        self.table.add_row(
            result.result,
            result.venue,
            str(result.our_score),
            str(result.opp_score),
            opp_name,
            result.match_date().strftime('%Y-%m-%d %H:%M'),
            result.notes(),
        )

    def print_match_table(self) -> None:
        self.console.print(self.table)
