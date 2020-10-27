FROM python:3

LABEL maintainer="gary@mc-williams.co.uk"

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-root

COPY . /app

RUN poetry install

CMD python main.py

ARG GIT_HASH
ENV GIT_HASH=${GIT_HASH:-dev}
