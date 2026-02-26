#!/usr/bin/env python

import sys
import logging
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

from rich.console import Console
from rich.table import Table

console = Console()

DEFAULT_INPUT_FILE: str = "matches.txt"


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class Match:
    venue: str
    opponent: str
    date: date


@dataclass
class Schedule:
    me: str
    output_filename: str
    duration: int
    start_time: str
    matches: list[Match]


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def setup_logging() -> logging.Logger:
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.FileHandler(log_dir / "generate.log", encoding="utf-8")],
    )
    return logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Opponent parsing
# ---------------------------------------------------------------------------

def parse_opponent(opponent: str) -> tuple[str, str | None]:
    """Split 'CLUB-TEAM' into (club, team), or return (opponent, None) if no team suffix."""
    if '-' in opponent:
        club, team = opponent.split('-', 1)
        return club, team
    return opponent, None


# ---------------------------------------------------------------------------
# Input parsing
# ---------------------------------------------------------------------------

def parse_header(lines: list[str]) -> tuple[str, str, int, date, str]:
    """Parse the 5 header lines and return (me, output_filename, duration, start_date, start_time)."""
    if len(lines) < 5:
        raise ValueError("Input file must have at least 5 header lines.")
    me = lines[0].strip()
    duration = int(lines[2].strip())
    date_parts = [int(p.strip()) for p in lines[3].split(',')]
    start_date = date(date_parts[0], date_parts[1], date_parts[2])
    output_filename = f"{lines[1].strip()}_games_{start_date.year}.yml"
    start_time = lines[4].strip()
    return me, output_filename, duration, start_date, start_time


def parse_match_line(line: str, current_date: date) -> Match:
    """Parse a single match line and return a Match with its calculated date."""
    parts = line.split()
    if len(parts) != 3:
        raise ValueError(f"Invalid match line (expected 3 fields): '{line}'")
    venue = parts[0].lower()
    opponent = parts[1]
    delta = int(parts[2])
    return Match(venue=venue, opponent=opponent, date=current_date + timedelta(days=delta))


def parse_matches(lines: list[str], start_date: date) -> list[Match]:
    """Parse all match lines and return a list of Match objects with accumulated dates."""
    matches: list[Match] = []
    current_date: date = start_date
    for line in lines:
        line = line.strip()
        if not line:
            continue
        match = parse_match_line(line, current_date)
        matches.append(match)
        current_date = match.date
    return matches


def load_schedule(input_path: str, logger: logging.Logger) -> Schedule:
    """Read and parse the input file, log the results, and return a Schedule."""
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]

    me, output_filename, duration, start_date, start_time = parse_header(lines)

    logger.info(f"  me:           {me}")
    logger.info(f"  output file:  {output_filename}")
    logger.info(f"  duration:     {duration}h")
    logger.info(f"  start date:   {start_date.strftime('%Y-%m-%d')}")
    logger.info(f"  start time:   {start_time}")

    matches = parse_matches(lines[5:], start_date)

    for m in matches:
        club, team = parse_opponent(m.opponent)
        team_suffix = f"  [team: {team}]" if team else ""
        logger.info(f"  match: {m.date.strftime('%Y-%m-%d')}  {m.venue:<4}  {club}{team_suffix}")

    return Schedule(me, output_filename, duration, start_time, matches)


# ---------------------------------------------------------------------------
# YAML output
# ---------------------------------------------------------------------------

def build_yaml(schedule: Schedule) -> str:
    """Build and return the YAML string from a Schedule."""
    lines: list[str] = [
        f"me: {schedule.me}",
        f"start_time: '{schedule.start_time}'",
        f"duration: {schedule.duration}",
        "matches:",
    ]
    for m in schedule.matches:
        club, team = parse_opponent(m.opponent)
        lines.append(f"- {m.venue}: {club}")
        if team:
            lines.append(f"  team: {team}")
        lines.append(f"  date: {m.date.strftime('%Y-%m-%d')}")
        lines.append(f"  our_score: 0")
        lines.append(f"  opp_score: 0")
    return "\n".join(lines) + "\n"


def write_yaml(schedule: Schedule, logger: logging.Logger) -> None:
    """Write the YAML file and display the match table."""
    yaml_str = build_yaml(schedule)
    with open(schedule.output_filename, 'w', encoding='utf-8') as f:
        f.write(yaml_str)
    logger.info(f"  output written: {schedule.output_filename}")
    print_table(schedule)
    console.print(f"\nWritten to [green]{schedule.output_filename}[/green]")


# ---------------------------------------------------------------------------
# Rich table display
# ---------------------------------------------------------------------------

def format_date_cell(match_date: date, normal_weekday: int) -> str:
    date_str = match_date.strftime('%a %d-%b')
    return f"[yellow]{date_str}[/yellow]" if match_date.weekday() != normal_weekday else date_str


def format_venue_cell(venue: str) -> str:
    return "[red]Home[/red]" if venue == 'home' else "[blue]Away[/blue]"


def format_opponent_cell(opponent: str) -> str:
    club, team = parse_opponent(opponent)
    return f"{club} [blue]({team})[/blue]" if team else club


def print_table(schedule: Schedule) -> None:
    table = Table(title=f"Schedule for {schedule.me}", show_lines=False, show_edge=True, header_style="bold")
    table.add_column("Date", style="cyan", no_wrap=True)
    table.add_column("Venue")
    table.add_column("Opponent")

    normal_weekday = schedule.matches[0].date.weekday()

    for m in schedule.matches:
        table.add_row(
            format_date_cell(m.date, normal_weekday),
            format_venue_cell(m.venue),
            format_opponent_cell(m.opponent),
        )

    console.print(table)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print(f"Usage: python generate.py [input.txt]  (default: {DEFAULT_INPUT_FILE})")
        sys.exit(1)

    input_file: str = sys.argv[1] if len(sys.argv) == 2 else DEFAULT_INPUT_FILE

    logger = setup_logging()
    logger.info(f"--- Generating from input: {input_file} ---")

    schedule = load_schedule(input_file, logger)
    write_yaml(schedule, logger)