#!/bin/bash

TEAM=${1:-fallsoutdoora}
YEAR=${2:-2022}

./docker-build.sh

docker run -p 5000:5000 \
    -e "ICAL_TEAM=${TEAM}" -e "ICAL_YEAR=${YEAR}" -e "ICAL_OUTPUT=/opt/ics-data" \
    -v "/mnt/d/Users/gmcwilliams/OneDrive/Documents/personal:/opt/ics-data" \
    garymcwilliams/ggbowlscalendar
