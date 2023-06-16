"""
Created on 13 Feb 2019

@author: gmcwilliams
"""
import json
import os
import sys
import logging

from pathlib import Path
from envparse import env


def savedir() -> Path:
    """
    Return a Path object for the savedir. If env ICAL_OUTPUT is set then use
    that, otherwise find the default dropbox path
    """
    if os.getenv("ICAL_OUTPUT") is not None:
        return Path(os.getenv("ICAL_OUTPUT"))

    try:
        if os.getenv("LOCALAPPDATA") is not None:
            path = Path(os.getenv("LOCALAPPDATA")) / "Dropbox" / "info.json"
        elif os.getenv("APPDATA") is not None:
            path = Path(os.getenv("APPDATA")) / "Dropbox" / "info.json"
        else:
            print("Could not find dropbox path")

        with open(str(path), "r", encoding="utf-8") as file_content:
            j = json.load(file_content)
        return Path(j["personal"]["path"]).absolute()
    except FileNotFoundError:
        print("info.json NotFound")


def _mk_save_dir() -> Path:
    newdir = Path(savedir() / "Apps" / "icalendar")

    if not newdir.exists():
        newdir.mkdir(parents=True)

    return newdir


def write_file(club: str, year: str, content: bytes) -> None:
    """Write the ics content to the created file."""
    filename = f"{club}_{year}.ics"
    newfile = _mk_save_dir() / filename
    newfile.write_bytes(content)
    logger = logging.getLogger(__name__)
    logger.info("saved:%s", newfile)


def find_file(folder: str, filename: str) -> Path:
    """
    Get a file. The base dir will be read from env var ICAL_DATAPATH.
    If ICAL_DATAPATH is not set then the value from the .env file will be used.
    If folder is provided it will be added to the Path.
    """
    env.read_envfile()

    if folder is None:
        data_path = Path(env.str("ICAL_DATAPATH"))
    else:
        data_path = Path(env.str("ICAL_DATAPATH"), folder)

    file = Path(data_path, filename)

    if not file.exists():
        print(f"Cannot find file: {file}")
        sys.exit(1)
    return file
