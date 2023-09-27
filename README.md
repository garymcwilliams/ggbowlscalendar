# Bowls Calendar [![GitHub CI][workflow-all]] [![CodeQL][codeql]] [![codecov.io][codecov-image]][codecov-link] [![Quality Gate Status][sonar-image]][sonar-link]

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


[workflow-all]: https://github.com/garymcwilliams/ggbowlscalendar/actions/workflows/workflow-all.yml/badge.svg?event=push
[codeql]: https://github.com/garymcwilliams/ggbowlscalendar/actions/workflows/workflow-linkql.yml/badge.svg?event=push
[codecov-image]: https://codecov.io/github/garymcwilliams/ggbowlscalendar/graph/badge.svg?token=EGNK0HBDQK
[codecov-link]: https://codecov.io/github/garymcwilliams/ggbowlscalendar
[sonar-image]: https://sonarcloud.io/api/project_badges/measure?project=garymcwilliams_ggbowlscalendar&metric=alert_status
[sonar-link]: https://sonarcloud.io/summary/new_code?id=garymcwilliams_ggbowlscalendar