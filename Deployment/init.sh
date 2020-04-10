sudo apt-get -y update
echo "Ubuntu packages updated"

sudo apt-get install -y python3-pip python3-dev
echo "Python Installed"

sudo apt-get install -y mongodb
echo "MongoDB Installed"

sudo apt-get install -y nginx
echo "nginx Installed"

sudo pip3 install virtualenv
echo "Virtual Environment Installed"

virtualenv flask/venv
. flask/venv/bin/activate
pip install --no-cache-dir -r ./flask/requirements.txt
deactivate
echo "All python packages installed"