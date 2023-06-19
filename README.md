# Bowls Calendar ![Python Test](https://github.com/garymcwilliams/ggbowlscalendar/workflows/Python%20Test/badge.svg) [![codecov](https://codecov.io/github/garymcwilliams/ggbowlscalendar/branch/main/graph/badge.svg?token=EGNK0HBDQK)](https://codecov.io/github/garymcwilliams/ggbowlscalendar) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=garymcwilliams_ggbowlscalendar&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=garymcwilliams_ggbowlscalendar)

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
