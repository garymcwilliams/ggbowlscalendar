#!/bin/bash

docker build -t ggbowlscalendar .
docker tag ggbowlscalendar:latest garymcwilliams/ggbowlscalendar:latest

# run docker-push.sh to push up to dockerhub
