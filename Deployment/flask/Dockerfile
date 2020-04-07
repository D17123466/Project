FROM python:3.7.2-stretch

WORKDIR /flask/app
ADD . /flask

RUN pip install --upgrade pip
RUN pip install setuptools --upgrade
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get install mongodb

# RUN mv /flask-app/gunicorn.service /etc/systemd/system/
# RUN systemctl start app
# RUN systemctl enable app


