FROM rocker/tidyverse

MAINTAINER Ralph Brecheisen <ralph.brecheisen@gmail.com>

COPY brainminer /var/www/brainminer/brainminer
COPY Rscripts /var/www/brainminer/Rscripts
COPY run_brainminer.sh /var/www/brainminer/run_brainminer.sh
COPY install_Python_packages.txt /var/www/brainminer/install_Python_packages.txt
COPY install_R_packages.R /var/www/brainminer/install_R_packages.R

WORKDIR /var/www/brainminer

RUN apt-get update \
    && apt-get install -yy \
        vim \
        curl \
        python2.7 \
        python2.7-dev \
        python-pip \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip \
    && pip install -r install_Python_packages.txt \
    && Rscript install_R_packages.R \
    && echo

CMD ["./run_brainminer.sh"]