#!/usr/bin/env bash

if [ "${1}" == "build" ]; then

    docker build -t brecheisen/brainminer .

elif [ "${1}" == "up" ]; then

    ./manage.sh down
	docker run -d --name brainminer -p 5000:5000 \
	    -v $(pwd)/brainminer:/var/www/brainminer/brainminer \
	    -v $(pwd)/R:/var/www/brainminer/R \
	    brecheisen/brainminer
	echo "BrainMiner is now running on http://localhost:5000"
	./manage.sh logs


elif [ "${1}" == "down" ]; then

	docker stop brainminer
    docker rm brainminer

elif [ "${1}" == "shell" ]; then

    docker exec -it brainminer /bin/bash

elif [ "${1}" == "logs" ]; then

    docker logs -f brainminer

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
    echo "After startup, BrainMiner will run on http://localhost:5000."

fi