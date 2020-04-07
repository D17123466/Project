# FROM python:3.7.2-stretch

# WORKDIR /flask-app
# ADD . /flask-app

# RUN pip install --upgrade pip
# RUN pip install setuptools --upgrade
# RUN pip install --no-cache-dir -r requirements.txt

# RUN apt-get install mongodb

# RUN mv /flask-app/gunicorn.service /etc/systemd/system/
# RUN systemctl start app
# RUN systemctl enable app



FROM ubuntu:latest

WORKDIR /flask-app
COPY . /flask-app

RUN apt-get update && apt-get install -y --no-install-recommends python3-pip python3-dev python3-virtualenv
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m virtualenv --python=/usr/bin/python3 $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir requirements.txt

RUN apt-get install -y gunicorn3

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
RUN echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' > tee /etc/apt/sources.list.d/mongodb.list
RUN apt-get update -y
RUN apt-get install -y mongodb
RUN mkdir -p /data/db
EXPOSE 27017

CMD ["gunicorn3", "--workers=3", "--bind","unix:gunicorn.sock", "-m", "007", "wsgi:app"]