@echo off

:: run for team specified by ICAL_TEAM env var
:: to set the team (or year) in powershell use $env:ICAL_TEAM = "name"

if "%ICAL_TEAM%"=="" goto no_team

docker run -p 5000:5000 -e "ICAL_TEAM=%ICAL_TEAM%" -e "ICAL_YEAR=2022" -e "ICAL_OUTPUT=/opt/ics-data" -v "D:/Users/gmcwilliams/OneDrive/Documents/personal:/opt/ics-data" garymcwilliams/ggbowlscalendar

::allow dynamic mount of app-data, HOWEVER we prefer to rebuild the image, with data in place on each edit
::-e "ICAL_DATAPATH=/app-data" -v "d:/dev/gitrepos/ggbowlscalendar-data:/app-data"  

::debug, gets a terminal to allow inspecting of the image contents
::docker run -p 5000:5000 -e "ICAL_TEAM=stcolmans" -e "ICAL_YEAR=2018-19" -e "ICAL_OUTPUT=/opt/ics-data" -v "C:/Users/gmcwilliams/Dropbox:/opt/ics-data" ggbowlscalendar /bin/bash
goto end

:no_team
echo set ICAL_TEAM to the teamn name

:end
