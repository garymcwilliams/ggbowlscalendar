from ggbowlscalendar.events import Events

import argparse
from envparse import env

env.read_envfile()

parser = argparse.ArgumentParser(description="Process Bowls matches.")
parser.add_argument("-t", "--team")
parser.add_argument("-y", "--year")

args = parser.parse_args()

team = args.team if args.team is not None else env('ICAL_TEAM')
year = args.year if args.year is not None else env('ICAL_YEAR')

events = Events(team, year)

events.add_events()
