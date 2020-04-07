sudo cp . /app
sudo apt-get update

sudo apt-get install python3-pip python3-dev mongodb nginx
sudo pip3 install virtualenv

virtualenv /app/flask/venv
flask/venv/bin/activate
pip install --no-cahche-dir -r /app/flask/requirements.txt
deactivate

