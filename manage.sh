#!/usr/bin/env bash

export PYTHON=${HOME}/.virtualenvs/brainminer/bin/python
export PYTHONPATH=$(pwd):${HOME}/.virtualenvs/brainminer/lib/python2.7:${HOME}/.virtualenvs/brainminer/lib/python2.7/site-packages
export PYTEST=${HOME}/.virtualenvs/brainminer/bin/py.test
export PYINSTALLER=${HOME}/.virtualenvs/brainminer/bin/pyinstaller
export UWSGI=${HOME}/.virtualenvs/brainminer/bin/uwsgi
export OPY=${HOME}/.virtualenvs/brainminer/lib/python2.7/site-packages/opy/opy.py

if [ "${1}" == "" ] || [ "${1}" == "help" ]; then

    echo "manage.sh <option>"
    echo ""
    echo "start-db"
    echo "start-server"
    echo "help"
    echo ""

elif [ "${1}" == "build" ]; then

    eval $(docker-machine env default)
    docker build -t brainminer/nginx:v1 ./nginx

elif [ "${1}" == "start" ]; then

    ./manage.sh package
    echo "Starting application server..."
    ${UWSGI} --http-socket 0.0.0.0:5000 --master --workers 1 --module brainminer.app:app --vacuum --die-on-term

elif [ "${1}" == "start-db" ]; then

    echo "Starting database..."

elif [ "${1}" == "package" ]; then

    echo "Packaging application..."
    rm -rf ./bin; mkdir ./bin
    ${PYINSTALLER} \
        --distpath ./bin/dist \
        --workpath ./bin/build \
        --specpath ./bin \
        --paths ./brainminer \
        --key jgbk4msytacvd5jv \
        --onedir --noconfirm --clean ./brainminer/app.py

else

    echo "Unknown command ${1}"

fi