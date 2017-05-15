FROM rocker/tidyverse

MAINTAINER Ralph Brecheisen <ralph.brecheisen@gmail.com>

COPY brainminer /var/www/brainminer/brainminer
COPY run_brainminer.sh /var/www/brainminer/run_brainminer.sh
COPY install_R_packages.R /var/www/brainminer/install_R_packages.R
COPY requirements.txt /tmp/requirements.txt

RUN apt-get update \
    && apt-get install -yy \
        vim \
        curl \
        python2.7 \
        python2.7-dev \
        python-pip \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip \
    && pip install -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt \
    && Rscript ./install_R_packages.R \
    && echo

WORKDIR /var/www/brainminer

CMD ["./run.sh"]