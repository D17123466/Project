sudo apt-get -y update

sudo apt-get install -y python3-pip python3-dev mongodb nginx
sudo pip3 install virtualenv

virtualenv flask/venv
. flask/venv/bin/activate
pip install --no-cache-dir -r ./flask/requirements.txt
deactivate


