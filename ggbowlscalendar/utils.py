"""
File and path utilities for the bowls calendar generator.
"""

import logging
import os
from pathlib import Path

import yaml
from envparse import env

LOGGER = logging.getLogger(__name__)


def get_output_dir() -> Path:
    """
    Return the directory where .ics files will be written.

    Reads ICAL_OUTPUT from the environment. Raises EnvironmentError if unset.
    """
    ical_output = os.getenv("ICAL_OUTPUT")
    if not ical_output:
        raise EnvironmentError(
            "ICAL_OUTPUT environment variable is not set. "
            "Set it to the directory where .ics files should be saved."
        )
    output_dir = Path(ical_output) / "Apps" / "icalendar"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def write_ical_file(filename: str, content: bytes) -> None:
    """Write *content* to *filename* inside the configured output directory."""
    dest = get_output_dir() / filename
    dest.write_bytes(content)
    LOGGER.info("Saved: %s", dest)


def find_data_file(filename: str, subfolder: str | None = None) -> Path:
    """
    Locate a data file under ICAL_DATAPATH (from env or .env file).

    Args:
        filename:  The file name, e.g. "teams.yml".
        subfolder: Optional sub-directory under ICAL_DATAPATH.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    env.read_envfile()
    base = Path(env.str("ICAL_DATAPATH"))
    path = base / subfolder / filename if subfolder else base / filename

    LOGGER.debug("find_data_file: %s", path)

    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")
    return path


def load_yaml(path: Path) -> dict:
    """Read and parse a YAML file, returning a dict."""
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_teams_data() -> dict:
    """Load teams.yml from the configured data path."""
    return load_yaml(find_data_file("teams.yml"))


def load_games_data(club: str, year: int | str) -> dict:
    """Load the games YAML for *club* and *year*."""
    return load_yaml(find_data_file(f"{club}_games_{year}.yml", subfolder=club))
