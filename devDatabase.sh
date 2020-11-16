#!/bin/bash
INFLUX_CONTAINER_NAME="influxdb-dev"

function start {
  # Start influxdb
  mkdir -p "$(pwd)"/db
  docker run --name "$INFLUX_CONTAINER_NAME" -d -p 8086:8086 -v "$(pwd)/db":/var/lib/influxdb influxdb
}

function stop {
  # Stop and remove influxdb
  echo "Stopping container $(docker stop $INFLUX_CONTAINER_NAME)"
  echo "Removing container $(docker rm $INFLUX_CONTAINER_NAME)"
}

function cleanup {
  # Delete db metadata
  rm -rf "$(pwd)"/db
}

"$@"
