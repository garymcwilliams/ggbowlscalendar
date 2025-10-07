# Copilot Instructions for ggbowlscalendar

## Project Overview
- This is a Python project for managing and generating bowls league calendars and results.
- Main code is in `ggbowlscalendar/` (core logic, results, teams, utilities).
- Data files (YAML) for teams, matches, and competitions are in `data/`.
- The `generate/` folder contains scripts for generating match data from text files.

## Key Workflows
- **Run main app:**
  - `python main.py --team <team name> --year <year>`
  - In VS Code, use Debug runtime (e.g., `fallsindoor`).
- **Generate data:**
  - `cd generate && python generate.py`
  - Requires a `matches.txt` file (see `generate/README.md` for format).
- **Manage dependencies:**
  - Use Poetry: `poetry update`, `poetry add <package>@latest`, `poetry add --dev <package>@latest`.

## Data Format Conventions
- YAML files in `data/` follow custom schemas for teams, matches, competitions.
- See `DataFormats.adoc` for details.
- Generated files use line-based `matches.txt` as input (see `generate/README.md`).

## Testing & Quality
- Tests are in `tests/` (e.g., `test_league_results_manager.py`).
- Coverage and quality are tracked via GitHub Actions, Codecov, and SonarCloud.

## Patterns & Conventions
- Core logic is modular: see `league_results_manager.py`, `team_manager.py`, `results_table_ical.py`, `results_table_printer.py`.
- Logging config: `logging.yml` (main app), `generate/logging.yml` (generator).
- Data is loaded from YAML files; changes to data schemas require updates in both code and sample files.
- For new leagues/teams, add YAML files in the appropriate subfolder under `data/`.

## Integration Points
- No external API calls; all data is local YAML.
- CI/CD via GitHub Actions (`workflow-all.yml`, `workflow-codeql.yml`).
- Poetry for dependency management.

## Examples
- To add a new team: create a YAML file in `data/<league>/` and update code in `team_manager.py` if new fields are needed.
- To generate a new season: prepare a `matches.txt` and run the generator script.

---
For more details, see `README.md` and `generate/README.md`. If conventions or workflows are unclear, ask for clarification or examples from maintainers.