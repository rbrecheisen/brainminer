#!/usr/bin/env bash

if [ "${1}" == "build" ]; then

    docker build -t brecheisen/brainminer .

elif [ "${1}" == "up" ]; then

    ./manage.sh down
	docker run -d --name brainminer -p 5000:5000 brecheisen/brainminer
	echo "BrainMiner is now running on http://localhost:5000. You can view the"
	echo "startup log by typing: docker logs brainminer".

elif [ "${1}" == "down" ]; then

	docker stop brainminer; docker rm brainminer

elif [ "${1}" == "start-worker" ]; then

    ./manage.sh stop-worker
    docker run -d --name rabbitmq --hostname my-rabbitmq -p 5672:5672 rabbitmq:3.6
    docker run -d --name redis -p 6379:6379 redis:3.0-alpine

elif [ "${1}" == "stop-worker" ]; then

    container=$(docker ps | grep rabbitmq:3.6 | awk '{print $1}')
    if [ "${container}" != "" ]; then
        docker stop ${container}; docker rm ${container}
    fi
    container=$(docker ps | grep redis:3.0-alpine | awk '{print $1}')
    if [ "${container}" != "" ]; then
        docker stop ${container}; docker rm ${container}
    fi

else

    echo "manage.sh <option>"
    echo ""
    echo "  build Builds Docker image."
    echo "  up    Starts container running BrainMiner."
    echo "  down  Stops and removes container."
    echo "  help  Shows this help."
    echo ""

fi