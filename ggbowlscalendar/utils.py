"""
Created on 13 Feb 2019

@author: gmcwilliams
"""
import json
import os
import sys

from envparse import env
from pathlib import Path


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

        with open(str(path)) as f:
            j = json.load(f)
        return Path(j["personal"]["path"]).absolute()
    except FileNotFoundError:
        print("info.json NotFound")


def get_match_file(club, year) -> Path:
    """
    Get the matches file for a given club/year.
    """
    return _get_file(club, f"{club}_matches_{year}.yml")


def get_games_file(club, year) -> Path:
    """
    Get the matches file for a given club/year.
    """
    return _get_file(club, f"{club}_games_{year}.yml")


def get_team_file(club) -> Path:
    return _get_file(club, f"{club}_teams.yml")


def get_teams_file() -> Path:
    return _get_file("teams.yml", None)


def _get_file(club, filename) -> Path:
    """
    Get a file. The base dir will be read from env var ICAL_DATAPATH.
    If ICAL_DATAPATH is not set then the value from the .env file will be used.
    """
    # env = Env(
    #    ICAL_DATAPATH=str,
    # )
    env.read_envfile()

    dataPath = Path(env.str("ICAL_DATAPATH"), club)
    if filename is None:
        file = Path(dataPath)
    else:
        file = Path(dataPath, filename)

    if not file.exists():
        print(f"Cannot find file: {file}")
        sys.exit(1)
    return file


def _get_match_schema(self):
    return strictyaml.Map(
        {
            "duration": strictyaml.Int(),
            "matches": strictyaml.Seq(
                strictyaml.Map(
                    {
                        "away": strictyaml.Str(),
                        "date": strictyaml.Str(),
                        "newdate": strictyaml.Str(),
                        "our_score": strictyaml.Int(),
                        "opp_score": strictyaml.Int(),
                    }
                )
            ),
        }
    )
