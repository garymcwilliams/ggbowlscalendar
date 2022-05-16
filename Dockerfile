FROM python:latest as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /app

FROM base as builder

ENV POETRY_HOME=/opt/poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN python -m venv /venv

COPY pyproject.toml poetry.lock ./
#RUN /opt/poetry/bin/poetry export -f requirements.txt | /venv/bin/pip install -r /dev/stdin
RUN /opt/poetry/bin/poetry install --no-root --no-dev

COPY . .
#RUN /opt/poetry/bin/poetry build && /venv/bin/pip install dist/*.whl
CMD ["/opt/poetry/bin/poetry", "run", "python3", "main.py"]

##FROM base as final

##LABEL maintainer="gary@mc-williams.co.uk"

##COPY --from=builder /venv /venv
##COPY docker-entrypoint.sh ./
##CMD ["./docker-entrypoint.sh"]
