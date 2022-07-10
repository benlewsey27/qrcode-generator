#!/bin/bash

# Example
#
# ./docker-compose.sh <command> <version>
# ./docker-compose.sh build 1.0.0

COMMAND=$1
VERSION=$2

ERROR_INVALID_ARG=1

if [ -z $1 ]; then
  echo "Error: command is unset!"
  exit $ERROR_INVALID_ARG
else
  if [ "$COMMAND" == "help" ]; then
    echo """Docker Compose Helper

A CLI helper to run docker-compose for the qrcode-generator project.

ARGUMENTS
command The docker compose command (Must be set to build, up or down).
version The version of the project to use.

EXAMPLE
./docker-compose.sh <command> <version>
./docker-compose.sh build 1.0.0
./docker-compose.sh up 1.0.0
"""
    exit 0
  fi

  if [ "$COMMAND" != "build" ] && [ "$COMMAND" != "up" ] && [ "$COMMAND" != "down" ]; then
    echo "Error: invalid value for command! It must be set to build, up or down."
    exit $ERROR_INVALID_ARG
  fi
fi

if [ -z $2 ]; then
  echo "Error: version is unset!"
  exit $ERROR_INVALID_ARG
fi

APP_VERSION=$VERSION docker compose $COMMAND
