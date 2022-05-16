#!/usr/bin/env bash

docker build -t ggbowlscalendar-app .
docker tag ggbowlscalendar-app:latest garymcwilliams/ggbowlscalendar-app:latest
docker push garymcwilliams/ggbowlscalendar-app:latest
