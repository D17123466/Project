FROM nginx

RUN sudo rm /etc/nginx/sites-enabled/default
RUN sudo mv /flask-app/nginx/nginx-conf /etc/nginx/sites-avaiable/

RUN sudo ln -s /etc/nginx/sites-avaiable/nginx-conf /etc/nginx/sites-enabled/
RUN sudo systemctl restart nginx
RUN sudo ufw allow 'Nginx Full'