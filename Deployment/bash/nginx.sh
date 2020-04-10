echo "server { listen 80; server_name "$1"; location / { include proxy_params; proxy_pass http://0.0.0.0:5000;} location /socket.io { include proxy_params; proxy_set_header Connection 'Upgrade'; proxy_pass http://0.0.0.0:5000/socket.io;}}" | tee /home/ubuntu/Project/Deployment/nginx/nginx_proxy
sudo rm -f /etc/nginx/sites-enabled/default
sudo rm -f /etc/nginx/sites-enabled/nginx_proxy
sudo rm -f /etc/nginx/sites-available/nginx_proxy
sudo cp /home/ubuntu/Project/Deployment/nginx/nginx_proxy /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/nginx_proxy /etc/nginx/sites-enabled/
sudo systemctl restart nginx
sudo systemctl status nginx
sudo ufw allow 'Nginx Full'