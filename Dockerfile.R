FROM rocker/tidyverse

MAINTAINER Ralph Brecheisen <ralph.brecheisen@gmail.com>

COPY brainminer /var/www/brainminer/brainminer
COPY run.sh /var/www/brainminer/run.sh
COPY requirements.txt /tmp/requirements.txt

RUN apt-get update \
    && apt-get install -yy \
        vim \
        curl \
        python2.7 \
        python2.7-dev \
        python-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip \
    && pip install -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt \
    && echo

WORKDIR /var/www/brainminer

CMD ["./run.sh"]