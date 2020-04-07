sudo apt-get install python3-pip python3-dev

sudo pip3 install virtualenv
virtualenv /home/ubuntu/Project/Deployment/flask/venv
source /home/ubuntu/Project/Deployment/flask/venv/bin/activate
pip install --no-cahche-dir -r /home/ubuntu/Project/Deployment/flask/requirements.txt
deactivate