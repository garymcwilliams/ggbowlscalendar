#!/usr/bin/env python

# generate match yml file

from datetime import date, timedelta
from rich.console import Console
from rich.table import Table


console = Console()
table = Table(show_header=True, header_style="bold magenta")


def print_header():
    table.add_column("date")
    table.add_column("venue")
    table.add_column("opp")


def print_where(where: str):
    colours = {'home': 'red', 'away': 'blue'}
    return f"[bold {colours[where]}]{where}[/]"


def print_match(curdate: date, where: str, opp: str):
    date_string = curdate.strftime('%Y-%m-%d')
    table.add_row(date_string, print_where(where), opp)


matchdata = []
idx = 0
print_header()
file = open("matches.txt", "r")
for line in file:
    if idx == 0:
        me = line.rstrip()
    elif idx == 1:
        filename = line.rstrip()
    elif idx == 2:
        duration = line.rstrip()
    elif idx == 3:
        year, month, day = line.split(",")
        curdate = date(int(year), int(month), int(day))
    elif idx == 4:
        start_time = line.rstrip()
    else:
        where, opp, delta = line.rstrip().split(" ")
        curdate = curdate + timedelta(days=int(delta))
        print_match(curdate, where, opp)
        matchdata.append(f"- {where}: {opp}")
        matchdata.append(f"  date: '{curdate}'")
        matchdata.append("  our_score: 0")
        matchdata.append("  opp_score: 0")
    idx += 1

savefile = f"{filename}.yml"
print(f"Saving {savefile}")
with open(f"{savefile}", 'w') as f:
    f.write(f"me: {me}\n")
    f.write(f"start_time: '{start_time}'\n")
    f.write(f"duration: {duration}\n")
    f.write("matches:\n")
    for item in matchdata:
        f.write(f"{item}\n")

console.print(table)
