FROM nginx

WORKDIR /nginx-app
COPY . /nginx-app

RUN rm /etc/nginx/default.conf
RUN mv nginx-conf /etc/nginx/conf.d/

# RUN ln -s /etc/nginx/sites-avaiable/nginx-conf /etc/nginx/sites-enabled/
# RUN systemctl restart nginx
# RUN ufw allow 'Nginx Full'
