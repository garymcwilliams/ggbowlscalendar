#!/usr/bin/env bash

docker run -p 5000:5000 -e "ICAL_OUTPUT=/app" -e "ICAL_TEAM=stcolmnans" -e "ICAL_YEAR=2018-19" ggbowlscalendar-app

