#!/usr/bin/env python

# generate match yml file
import logging
import logging.config
import os
from datetime import date, timedelta
import yaml
from rich.console import Console
from rich.table import Table


console = Console()
table = Table(show_header=True, header_style="bold magenta")


def print_header():
    """define the table header"""
    table.add_column("date")
    table.add_column("venue")
    table.add_column("opp")


def where_str(match_where: str):
    """print home/away in different colours"""
    colours = {'home': 'red', 'away': 'blue'}
    return f"[bold {colours[match_where]}]{match_where}[/]"


def print_match(match_curdate: date, match_where: str, match_opp: str):
    """add a match row to table"""
    date_pattern = '%a %d-%b'
    date_string = match_curdate.strftime(date_pattern)
    table.add_row(date_string, where_str(match_where), match_opp)
    logger.debug("(%s) (%s) (%-5s)", date_string, match_where, match_opp)


def setup_logging(
    default_path='logging.yml',
    default_level=logging.INFO,
):
    """Setup logging configuration """
    path = default_path
    if os.path.exists(path):
        with open(path, "rt", encoding="utf-8") as config:
            config = yaml.safe_load(config.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


setup_logging()

logger = logging.getLogger(__name__)
logger.debug("===============================generating======================")

matchdata = []
MATCH_LINE = 0
print_header()
file = open("matches.txt", "r", encoding="UTF-8")
FILENAME = None
START_TIME = None
DURATION = None
for line in file:
    if MATCH_LINE == 0:
        me = line.rstrip()
        logger.debug("me=%s", me)
    elif MATCH_LINE == 1:
        FILENAME = line.rstrip()
    elif MATCH_LINE == 2:
        DURATION = line.rstrip()
        logger.debug("duration=%s", DURATION)
    elif MATCH_LINE == 3:
        year, month, day = line.split(",")
        curdate = date(int(year), int(month), int(day))
        logger.debug("start_date=%s", curdate)
    elif MATCH_LINE == 4:
        START_TIME = line.rstrip()
        logger.debug("start_time=%s", START_TIME)
    else:
        where, opp, delta = line.rstrip().split(" ")
        curdate = curdate + timedelta(days=int(delta))
        print_match(curdate, where, opp)
        matchdata.append(f"- {where}: {opp}")
        matchdata.append(f"  date: '{curdate}'")
        matchdata.append("  our_score: 0")
        matchdata.append("  opp_score: 0")
    MATCH_LINE += 1

savefile = f"{FILENAME}.yml"
logger.debug("Saving %s", savefile)
with open(f"{savefile}", 'w', encoding="UTF-8") as yaml_file:
    yaml_file.write(f"me: {me}\n")
    yaml_file.write(f"start_time: '{START_TIME}'\n")
    yaml_file.write(f"duration: {DURATION}\n")
    yaml_file.write("matches:\n")
    for item in matchdata:
        yaml_file.write(f"{item}\n")

console.print(table)
logger.info("Saved %s", savefile)

logger.debug("done")
