FROM python:3.7.2-stretch

WORKDIR /flask-app
ADD . /flask-app

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN pip install --upgrade pip
RUN pip3 install virtualenv
RUN virtualenv venv
RUN source venv/bin/activate
RUN pip install setuptools --upgrade
RUN pip install --no-cache-dir -r requirements.txt
RUN deactivate

RUN apt-get install mongodb

RUN mv /flask-app/gunicorn.service /etc/systemd/system/
RUN systemctl start app
RUN systemctl enable app


