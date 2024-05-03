#!/usr/bin/env bash
# This script sets up your web servers for the deployment of web_static

apt-get -y update
apt-get -y install nginx

mkdir --parents /data/web_static/shared/
mkdir --parents /data/web_static/releases/test/

echo -e "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

ln -sf /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu /data/
chgrp -R ubuntu /data/

echo -e "\nserver {

	listen 80 default_server;
	listen [::]:80 default_server;
	root	/var/www/html;
	index index.html;
	add_header X-Served-By $HOSTNAME;

	location /hbnb_static {
		alias /data/web_static/current;
		index index.html;
	}

	location /redirect_me {
		return 301 https://www.youtube.com/watch?v=dQw4w9WgXcQ;
	}

	error_page 404 /error_404.html;
	location /error_404 {
		root /var/www/html;
		internal;
	}

}" > /etc/nginx/sites-available/default

service nginx restart
