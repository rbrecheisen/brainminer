FROM python:2.7

MAINTAINER Ralph Brecheisen <ralph.brecheisen@gmail.com>

COPY brainminer /var/www/brainminer/brainminer
COPY R /var/www/brainminer/R
COPY run_brainminer.sh /var/www/brainminer/run_brainminer.sh
COPY install_Python_packages.txt /var/www/brainminer/install_Python_packages.txt
COPY install_R_packages.R /var/www/brainminer/install_R_packages.R

WORKDIR /var/www/brainminer

RUN apt-get update \
    && apt-get install -yy vim curl \
    && apt-get install -yy r-base \
    && pip install --upgrade pip \
    && pip install -r install_Python_packages.txt \
    && Rscript install_R_packages.R

CMD ["./run_brainminer.sh"]