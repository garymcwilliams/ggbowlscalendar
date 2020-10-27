#!/usr/bin/env bash

docker build --build-arg GIT_HASH=${GIT_HASH::7} -t ggbowlscalendar-app .
docker tag ggbowlscalendar-app:latest garymcwilliams/ggbowlscalendar-app:latest
docker push garymcwilliams/ggbowlscalendar-app:latest
