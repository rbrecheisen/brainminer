#!/usr/bin/env bash

########################################################################################################################
# HELP
########################################################################################################################
if [ "${1}" == "" ] || [ "${1}" == "help" ]; then

    echo "manage.sh <option>"
    echo ""
    echo "start-worker"
    echo "stop-worker"
    echo "help"
    echo ""

########################################################################################################################
# START WORKER
########################################################################################################################
elif [ "${1}" == "start-worker" ]; then

    ./manage.sh stop-worker
    docker run -d --name rabbitmq --hostname my-rabbitmq -p 5672:5672 rabbitmq:3.6
    docker run -d --name redis -p 6379:6379 redis:3.0-alpine

########################################################################################################################
# STOP WORKER
########################################################################################################################
elif [ "${1}" == "stop-worker" ]; then

    container=$(docker ps | grep rabbitmq:3.6 | awk '{print $1}')
    if [ "${container}" != "" ]; then
        docker stop ${container}; docker rm ${container}
    fi
    container=$(docker ps | grep redis:3.0-alpine | awk '{print $1}')
    if [ "${container}" != "" ]; then
        docker stop ${container}; docker rm ${container}
    fi
fi