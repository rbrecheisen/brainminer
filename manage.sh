#!/usr/bin/env bash

export PYTHON=$HOME/.virtualenvs/brainminer/bin/python
export PYTHONPATH=$(pwd)

if [ "${1}" == "" ] || [ "${1}" == "help" ]; then

    echo "manage.sh <option>"
    echo ""
    echo "start-db"
    echo "start-server"
    echo "help"
    echo ""

elif [ "${1}" == "start-db" ]; then

    echo "Starting database..."

elif [ "${1}" == "start-server" ]; then

    echo "Starting application server..."

else

    echo "Unknown command ${1}"

fi