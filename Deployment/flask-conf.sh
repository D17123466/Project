sudo cp /home/ubuntu/Project/Deployment/flask/gunicorn.service /etc/systemd/system/
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn
