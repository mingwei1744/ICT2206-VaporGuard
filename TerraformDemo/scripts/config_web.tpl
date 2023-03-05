#!/bin/bash
# Script3. Web setting configurations

root="${rootUser}"
domain="${domainName}"
email="${emailAddress}"

timestamp=`date "+%Y-%m-%d %H:%M:%S"`
log="/home/$root/config.log"

function install_pkg() {
  apt-get -y install $1

  if [ $? -eq 0 ]; then
    echo "$timestamp Installed $1" >> $log
  else
    echo "$timestamp Failed to install $1" >> $log
  fi
}

function execute_chk() {
  eval "$1"

  if [ $? -eq 0 ]; then
    echo "$timestamp Success: $1"
  else
    echo "$timestamp Failed: $1"
  fi
}

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
# sudo fuser -k 443/tcp
# sudo systemctl restart nginx