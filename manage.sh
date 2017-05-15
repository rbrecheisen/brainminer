#!/usr/bin/env bash

if [ "${1}" == "build" ]; then

    docker build -t brecheisen/brainminer .

elif [ "${1}" == "up" ]; then

    ./manage.sh down
	docker run -d --name brainminer -p 5000:5000 \
	    -v $(pwd)/brainminer:/var/www/brainminer/brainminer \
	    -v $(pwd)/Rscripts:/var/www/brainminer/Rscripts \
	    brecheisen/brainminer
	echo "BrainMiner is now running on http://localhost:5000"
	./manage.sh logs


elif [ "${1}" == "down" ]; then

	docker stop brainminer; docker rm brainminer

elif [ "${1}" == "shell" ]; then

    docker exec -it brainminer /bin/bash

elif [ "${1}" == "logs" ]; then

    docker logs -f brainminer

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
    echo "  shell Enters a bash shell inside the container."
    echo "  logs  Shows trailing log of the container."
    echo "  help  Shows this help."
    echo ""

fi