FROM ubuntu:18.04

WORKDIR /home/app

# apt
RUN apt-get update && \
  apt-get install \
    sudo \
    curl \
    wget \
    git \
    zip \
    unzip \
    python3 \
    python3-pip \
    python3-psycopg2 \
    libpq-dev \
    -y

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

COPY app .

RUN pip3 install -r requirements.txt

CMD uwsgi --ini uwsgi.ini