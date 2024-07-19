#!/usr/bin/env bash
#Sets up the webserver for deployment

sudo apt-get update
sudo apt-get install -y nginx
sudo service nginx start

sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
" | sudo tee /data/web_static/releases/test/index.html > /dev/null

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

dataloc='\\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}'
sudo sed -i "43i ${dataloc}" /etc/nginx/sites-available/default

sudo service nginx restart
