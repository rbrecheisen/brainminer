#!/usr/bin/env bash

########################################################################################################################
# INSTALL APP
########################################################################################################################
if [ "${1}" == "build" ]; then

    docker build -t brecheisen/brainminer .

########################################################################################################################
# START APP
########################################################################################################################
elif [ "${1}" == "up" ]; then

    ./manage.sh down

	docker run -d --name brainminer -p 80:5000 brecheisen/brainminer

########################################################################################################################
# STOP APP
########################################################################################################################
elif [ "${1}" == "down" ]; then

	docker stop brainminer; docker rm brainminer

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

########################################################################################################################
# SHOW HELP
########################################################################################################################
else

    echo "manage.sh <option>"
    echo ""
    echo "build"
    echo "up"
    echo "down"
    echo "start-worker"
    echo "stop-worker"
    echo "help"
    echo ""

fi