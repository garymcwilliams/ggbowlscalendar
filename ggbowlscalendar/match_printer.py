from rich.console import Console
from rich.table import Table


console = Console()
table = Table(show_header=True, header_style="bold magenta")


def add_match_to_table(
                result,
                venue,
                match_date,
                me,
                our_score,
                opp_score,
                opp,
                notes: str = "",
        ):
    table.add_row(result, venue, str(our_score), str(opp_score),
                  opp, match_date.strftime('%Y-%m-%d'), notes)


def print_table_header():
    table.add_column("R")
    table.add_column("venue")
    table.add_column("Us")
    table.add_column("Op")
    table.add_column("opp")
    table.add_column("date")
    table.add_column("note")


def print_match_table():
    console.print(table)