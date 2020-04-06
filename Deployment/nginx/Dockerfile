FROM nginx

WORKDIR /nginx-app
ADD . /nginx-app

RUN rm /etc/nginx/sites-enabled/default
RUN mv nginx-conf /etc/nginx/sites-avaiable/

RUN ln -s /etc/nginx/sites-avaiable/nginx-conf /etc/nginx/sites-enabled/
RUN systemctl restart nginx
RUN ufw allow 'Nginx Full'
