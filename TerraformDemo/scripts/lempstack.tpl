#!/bin/bash
timestamp=`date "+%Y-%m-%d %H:%M:%S"`
log="/home/adminuser/lempstack-install.log"
touch /home/adminuser/lempstack-install.log

domain="INSERTYOURDOMAINHERE"

sudo apt update -y
#===================================================================#
# Create new user
#===================================================================#
sudo useradd webadm
sudo usermod -aG sudo webadm
echo "$timestamp Created webadm user" >> $log
#===================================================================#
# Configure firewall #TODO
#===================================================================#
# sudo ufw limit ssh
# sudo ufw enable

# # Write configs to sshd_config
# sudo echo "
# PermitRootLogin no
# PasswordAuthentication no
# AllowUsers adminuser" >> /etc/ssh/sshd_config 

# # Configure SSH to run on port 1002
# sudo ufw limit 1002/tcp
# sudo echo "Port 1002" >> /etc/ssh/sshd_config

# sudo systemctl restart ssh

#===================================================================#
# Install LEMP Stack
#===================================================================#
# Install Nginx
sudo apt install nginx-extras -y
sudo ufw allow 'Nginx Full'
echo "$timestamp Installed Nginx" >> $log

# Install MariaDB
sudo apt install mariadb-server -y

# # mysql_secure_installation #TODO
# # Setting the root password
# sudo mysql -e "UPDATE mysql.user SET Password = PASSWORD('xia0Ming') WHERE User = 'root'"
# # Remove anonymous users
# sudo mysql -e "DROP USER ''@'$(hostname)'"
# # Remove test database and access to it
# sudo mysql -e "DROP DATABASE test"
# # Make changes take effect
# sudo mysql -e "FLUSH PRIVILEGES"

echo "$timestamp Installed MariaDB" >> $log

# Install PHP
sudo apt install php-fpm php-mysql -y
sudo cp -a -v /etc/nginx/sites-available/default /etc/nginx/sites-available/$domain
sudo chmod 666 /etc/nginx/sites-available/$domain
sudo echo "
server {
        listen 80;
        listen [::]:80;

        root /var/www/html;

        # Add index.php to the list if you are using PHP
        index index.php index.html index.htm index.nginx-debian.html;

        server_name $domain;

        location / {
                # First attempt to serve request as file, then
                # as directory, then fall back to displaying a 404.
                try_files \$uri \$uri/ =404;
        }

        # pass PHP scripts to FastCGI server
        #
        location ~ \.php$ {
                include snippets/fastcgi-php.conf;

                # With php-fpm (or other unix sockets):
                fastcgi_pass unix:/var/run/php/php7.4-fpm.sock;
        #       # With php-cgi (or other tcp sockets):
        #       fastcgi_pass 127.0.0.1:9000;
        }

        # deny access to .htaccess files, if Apache's document root
        # concurs with nginx's one
        #
        location ~ /\.ht {
                deny all;
        }
}" > /etc/nginx/sites-available/$domain
sudo chmod 644 /etc/nginx/sites-available/$domain
sudo ln -s /etc/nginx/sites-available/$domain /etc/nginx/sites-enabled/
sudo unlink /etc/nginx/sites-enabled/default
sudo systemctl restart nginx

sudo chown -R adminuser:adminuser /var/www/html
sudo chmod 2775 /var/www/html

sudo echo "
<!DOCTYPE html>
<html>
        <body style='background-color:red'>
                <h1 style='text-align:center'> ICT2206 CLOUD-INIT AUTOMATION TEST <h1>

                <?php echo \"<h3 style='text-align:center'> PHP interpreter successfully installed </h3>\"; ?>
        </body>
</html>" > /var/www/html/index.php

echo "$timestamp Installed PHP" >> $log

#===================================================================#
# Setting up HTTPS using let's encrypt cert
# Commented out to prevent over usage of let's encrypt cert, uncomment to test
#===================================================================#
# sudo snap install core
# sudo snap refresh core
# sudo snap install --classic certbot

# sudo certbot --nginx -d $domain --email $email --agree-tos
# sudo systemctl restart nginx

#===================================================================#
# Enable HTTP/2 
# Commented out to prevent over usage of let's encrypt cert, uncomment to test
#===================================================================#
# sudo sed -i 's/443 ssl ipv6only=on;/443 ssl http2 ipv6only=on;/' /etc/nginx/sites-available/$domain
# sudo sed -i 's/listen 443 ssl;/listen 443 ssl http2;/' /etc/nginx/sites-available/$domain

#===================================================================#
# Enable HSTS
# Commented out to prevent over usage of let's encrypt cert, uncomment to test
#===================================================================#
# sudo sed -i '/^http {/a \       add_header Strict-Transport-Security "max-age=15768000; includeSubDomains" always;' /etc/nginx/nginx.conf