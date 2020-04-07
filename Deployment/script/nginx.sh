sudo apt-get install nginx 

echo "server { listen 80; server_name "$1"; location / { include proxy_params; proxy_pass http://unix:/home/ubuntu/Project/Deployment/flask/gunicorn.sock:;}}" | tee nginx_proxy

sudo rm /etc/nginx/sites-enabled/default
sudo cp /home/ubuntu/Project/Deployment/nginx/nginx_proxy /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/nginx_proxy /etc/nginx/sites-enabled/
sudo systemctl restart nginx
sudo ufw allow 'Nginx Full'

