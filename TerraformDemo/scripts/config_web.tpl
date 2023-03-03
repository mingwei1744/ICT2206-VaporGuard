#!/bin/bash
# Script3. Web setting configurations

timestamp=`date "+%Y-%m-%d %H:%M:%S"`
log="/home/adminuser/config.log"

domain="${domainName}"

#===================================================================#
# Setting up HTTPS and HTTP/2 #TODO
#===================================================================#
# sudo snap install core
# sudo snap refresh core
# sudo snap install --classic certbot

# sudo certbot --nginx -d $domain
# sudo systemctl restart nginx
