# Pull python image
FROM ubuntu

FROM python:3.6

# Set work directory
WORKDIR /home/Project/Deployment

# Install
RUN sudo apt-get update 
RUN sudo apt-get python3-pip, python3-dev, nginx
RUN sudo pip3 install virtualenv
RUN virtualenv venv
RUN source venv/bin/activate
RUN pip install --no-cache-dir -r requirements.txt



