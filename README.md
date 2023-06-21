# Bowls Calendar [![GitHub CI](https://github.com/garymcwilliams/ggbowlscalendar/actions/workflows/workflow-all.yml/badge.svg?branch=garymcwilliams/issue43-main-merge)](https://github.com/garymcwilliams/ggbowlscalendar/actions/workflows/workflow-all.yml) [![codecov](https://codecov.io/github/garymcwilliams/ggbowlscalendar/branch/garymcwilliams/issue43-main-merge/graph/badge.svg?token=EGNK0HBDQK)](https://codecov.io/github/garymcwilliams/ggbowlscalendar/tree/garymcwilliams%2Fissue43-main-merge) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=garymcwilliams_ggbowlscalendar&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=garymcwilliams_ggbowlscalendar&branch=garymcwilliams%2Fissue43-main-merge) [![CodeQL](https://github.com/garymcwilliams/ggbowlscalendar/actions/workflows/workflow-codeql.yml/badge.svg?branch=garymcwilliams%2Fissue43-main-merge)](https://github.com/garymcwilliams/ggbowlscalendar/actions/workflows/workflow-codeql.yml)

## Running

### command line

```bash
cd src
python main.py --team <team name> --year <year>
```

### In VS Code

Select a Debug runtime (from Debug side window), e.g. `fallsindoor`

## Data Formats

see link: [![icalendar-data](https://github.com/garymcwilliams/icalendar-data)]

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
