@echo off

docker run -it --rm -p 5000:5000 -e "ICAL_TEAM=stcolmans" -e "ICAL_YEAR=2019-20" -e "ICAL_OUTPUT=/opt/ics-data" -v "D:/Users/gmcwilliams/OneDrive/Documents/personal:/opt/ics-data" --entrypoint="/bin/bash" garymcwilliams/ggbowlscalendar
