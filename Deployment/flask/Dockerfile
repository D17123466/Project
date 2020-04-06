FROM python:3.7.2-stretch

WORKDIR /flask-app/flask

ADD /home/ubuntu/Project/Deployment/ /flask-app

RUN sudo pip3 install virtualenv
RUN virtualenv venv
RUN source venv/bin/activate
RUN pip install --no-cache-dir -r requirements.txt
RUN deactivate

RUN sudo apt-get install mongodb

RUN sudo mv /flask-app/flask/gunicorn.service /etc/systemd/system/
RUN sudo systemctl start app
RUN sudo systemctl enable app


