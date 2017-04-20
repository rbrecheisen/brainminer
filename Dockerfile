FROM python:2.7

MAINTAINER Ralph Brecheisen <ralph.brecheisen@gmail.com>

COPY brainminer /var/www/brainminer
COPY run.sh /var/www/brainminer/run.sh
COPY requirements.txt /tmp/requirements.txt

RUN apt-get update && apt-get install -yy vim curl \
    && pip install --upgrade pip \
    && pip install -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt \
    && echo

WORKDIR /var/www/brainminer

CMD ["./run.sh"]