@echo off

docker build -t ggbowlscalendar .
docker tag ggbowlscalendar:latest garymcwilliams/ggbowlscalendar:latest
docker push garymcwilliams/ggbowlscalendar:latest
