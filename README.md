= Bowls Calendar image:https://github.com/garymcwilliams/ggbowlscalendar/workflows/Python%20Test/badge.svg["Coverage", link="https://github.com/garymcwilliams/ggbowlscalendar/actions"] image:https://github.com/garymcwilliams/ggbowlscalendar/workflows/CodeQL/badge.svg["CodeQL", link="https://github.com/garymcwilliams/ggbowlscalendar/actions"]

== Running

=== command line
[source]
----
cd src
python main.py --team <team name> --year <year>
----

=== In VS Code
Select a Debug runtime (from Debug side window), e.g. `fallsindoor`

== Data Formats
see link:https://github.com/garymcwilliams/icalendar-data[icalendar-data]

= Managing python pip dependencies
```
poetry upgrade
```
