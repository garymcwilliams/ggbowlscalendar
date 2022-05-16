docker run -p 5000:5000 -e "ICAL_DATAPATH=d:/dev/gary/gitrepos/icalendar-data" -e "ICAL_OUTPUT=/app" -e "ICAL_TEAM=stcolmans" -e "ICAL_YEAR=2019-20" garymcwilliams/ggbowlscalendar-app
::docker run -p 5000:5000 -e "ICAL_OUTPUT=/opt/ics-data" -e "ICAL_TEAM=stcolmans" -e "ICAL_YEAR=2019-20" -v "D:/Users/gmcwilliams/OneDrive/Documents/personal:/opt/ics-data" --entrypoint="/bin/bash" garymcwilliams/ggbowlscalendar

