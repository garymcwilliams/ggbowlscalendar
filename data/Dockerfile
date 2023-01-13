FROM garymcwilliams/ggbowlscalendar-app

LABEL maintainer gary@mc-williams.co.uk

WORKDIR /app-data

# copy current data, requires docker-build on each edit of data
COPY . ./

ENV ICAL_DATAPATH /app-data

# reset dir to the main app folder
WORKDIR /app
