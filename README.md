# Bowls Calendar ![Python Test](https://github.com/garymcwilliams/ggbowlscalendar/workflows/Python%20Test/badge.svg) ![CodeQL](https://github.com/garymcwilliams/ggbowlscalendar/workflows/CodeQL/badge.svg) ![SonarCloud](https://sonarcloud.io/api/project_badges/measure?project=garymcwilliams_ggbowlscalendar&metric=alert_status)

## Running

### command line

```bash
cd src
python main.py --team <team name> --year <year>
```

### In VS Code

Select a Debug runtime (from Debug side window), e.g. `fallsindoor`

## Data Formats

see link: ![icalendar-data](https://github.com/garymcwilliams/icalendar-data)

## Managing python poetry dependencies

```bash
poetry update
```

To update depd in `pyproject.yaml`, for each listed package run

```bash
poetry add pylint@latest
```

for `dev` dependencies use

```bash
poetry add --dev pytest@latest
```
