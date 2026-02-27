"""
Created on 13 Feb 2019

@author: gmcwilliams
"""
import json
import os
import sys
import logging
from pathlib import Path

import yaml

from envparse import env


LOGGER = logging.getLogger(__name__)


def savedir() -> Path:
    """
    Return a Path object for the savedir. If env ICAL_OUTPUT is set then use
    that, otherwise find the default dropbox path
    """
    ical_output = os.getenv("ICAL_OUTPUT")
    if ical_output is None:
        raise EnvironmentError("ICAL_OUTPUT environment variable is not set")
    return Path(ical_output)

def _mk_save_dir() -> Path:
    newdir = Path(savedir() / "Apps" / "icalendar")

    if not newdir.exists():
        newdir.mkdir(parents=True)

    return newdir


def write_ical_file(filename: str, content: bytes) -> None:
    """Write the ics content to the named file. Create file if necessary"""
    newfile = _mk_save_dir() / filename
    newfile.write_bytes(content)
    LOGGER.info("saved:%s", newfile)


def find_file(filename: str, folder: str = None) -> Path:
    """
    Get a file path. The base dir will be read from env var ICAL_DATAPATH.
    If ICAL_DATAPATH is not set then the value from the .env file will be used.
    If folder is provided it will be added to the Path.
    """
    env.read_envfile()

    if folder is None:
        LOGGER.debug("find_file=%s", filename)
        data_path = Path(env.str("ICAL_DATAPATH"))
    else:
        LOGGER.debug("find_file=%s in %s", filename, folder)
        data_path = Path(env.str("ICAL_DATAPATH"), folder)

    file_path = Path(data_path, filename)

    if not file_path.exists():
        LOGGER.error("Cannot find file: %s", file_path)
        raise FileNotFoundError(f"Cannot find file: {file_path}")
    return file_path


def get_teams_data() -> dict:
    """
    Get the teams Path
    """
    teams_path = find_file("teams.yml")
    return read_yaml_data(teams_path)


def get_games_data(club, year) -> dict:
    """
    Get the matches Path for a given club/year.
    """
    games_path = find_file(f"{club}_games_{year}.yml", club)
    return read_yaml_data(games_path)


def read_yaml_data(yaml_path: Path) -> dict:
    """
    read the yaml from file into a dict
    """
    with open(yaml_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return data
