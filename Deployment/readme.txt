1. AWS

2. Ubuntu

-> sudo apt-get update
-> sudo apt-get install python3-pip python3-dev nginx
-> sudo pip3 install virtualenv
-> sudo apt-get install -y docker.io
-> git clone https://github.com/D17123466/Project.git
-> cd Project/Deployment
-> virtualenv venv 
-> source venv/bin/activate
-> pip install --no-cache-dir -r requirements.txt
-> deactivate

-> sudo vim /etc/systemd/system/app.service
-> sudo systemctl start app
-> sudo systemctl enable app

-> sudo rm /etc/nginx/sites-enabled/default
-> sudo vim /etc/nginx/sites-available/app

-> sudo ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled
-> sudo systemctl restart nginx 
-> sudo ufw allow 'Nginx Full'