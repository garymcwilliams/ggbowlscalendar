#!/usr/bin/env bash

docker run \
    -e "TEAM=stcolmnans" -e "YEAR=2018-19" \
    --volume "//c/Users/gmcwilliams/OneDrive/Documents/personal:/app/ics-data" \
    --volume "//d/dev/gary/gitrepos/icalendar-data:/app/icalendar-data" \
    --rm -it icalendar-app bash