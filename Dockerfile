# check from: https://stackoverflow.com/questions/53835198/integrating-python-poetry-with-docker


FROM python:3.9-slim-buster as base

LABEL maintainer="gary@mc-williams.co.uk"

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN addgroup --gid 10001 calendar && adduser --uid 10000 --system --ingroup calendar --home /home/calendar calendar
RUN chown -R calendar:calendar /app

FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.4

RUN pip install "poetry==$POETRY_VERSION"

USER calendar

RUN python -m venv /app/venv

COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt | /app/venv/bin/pip install -r /dev/stdin

COPY --chown=calendar:calendar . .
COPY --chown=calendar:calendar .env.docker .env
RUN poetry build && /app/venv/bin/pip install dist/*.whl

FROM base as final

COPY --chown=calendar:calendar --from=builder /app/ /app/
COPY --chown=calendar:calendar docker-entrypoint.sh .
CMD ["./docker-entrypoint.sh"]

ARG GIT_HASH
ENV GIT_HASH=${GIT_HASH:-dev}
ARG TEAM
ENV ICAL_TEAM=${TEAM:-stcolmans}
ARG YEAR
ENV ICAL_YEAR=${YEAR:-2018-19}
ENV ICAL_DATAPATH=/app/icalendar-data
ENV ICAL_OUTPUT=/app/ics-data
