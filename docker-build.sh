#!/usr/bin/env bash

export GIT_HASH=$(git rev-parse HEAD)
docker build --build-arg GIT_HASH=${GIT_HASH::7} -t ggbowlscalendar-app .
docker tag ggbowlscalendar-app:latest garymcwilliams/ggbowlscalendar-app:latest
docker push garymcwilliams/ggbowlscalendar-app:latest
