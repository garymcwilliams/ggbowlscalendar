from rich.console import Console
from rich.table import Table
from .match import Match


console = Console()
table = Table(show_header=True, header_style="bold magenta")


def add_match(match: Match):
    table.add_row(match.result, match.home_team_name, match.home_score, match.away_score,
        match.away_team_name, match.display_date(), f"{match.label} {match.warning}")


def print_header():
    table.add_column("R")
    table.add_column("home")
    table.add_column("S")
    table.add_column("S")
    table.add_column("away")
    table.add_column("date")
    table.add_column("note")


def print_matches():
    console.print(table)