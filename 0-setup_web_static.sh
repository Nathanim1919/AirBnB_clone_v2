#!/usr/bin/env bash
# Setup web server for deployment
sudo apt-get install -y nginx > /dev/null

mkdir -p /data/web_static/releases/
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/

file="<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>"
echo "$file" > /data/web_static/releases/test/index.html

link='/data/web_static/current'
target='/data/web_static/releases/test/'
if [ -L "$link" ]; then
    sudo rm "$link"
fi
sudo ln -s "$target" "$link"

sudo chown -R ubuntu:ubuntu /data

location="\n\tlocation /hbnb_static {\n\
\t\talias /data/web_static/current/;\n\t}"
sudo sed -i "/server_name _;/a \ $location" /etc/nginx/sites-available/default

sudo service nginx restart > /dev/null
