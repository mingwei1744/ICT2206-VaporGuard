#!/bin/bash
# Script1. Server configurations

timestamp=`date "+%Y-%m-%d %H:%M:%S"`
log="/home/adminuser/config.log"
touch $log
root="${rootUser}"

sudo apt update -y
#===================================================================#
# Create new user
#===================================================================#
sudo useradd "${webUser}"
sudo usermod -aG sudo "${webUser}"
echo "$timestamp Created "${webUser}" user" >> $log

#===================================================================#
# Configure firewall #TODO
#===================================================================#
# sudo ufw limit ssh
# sudo ufw enable

# # Write configs to sshd_config
# sudo echo "
# PermitRootLogin no
# PasswordAuthentication no
# AllowUsers $root" >> /etc/ssh/sshd_config 

# # Configure SSH to run on port 1002
# sudo ufw limit 1002/tcp
# sudo echo "Port 1002" >> /etc/ssh/sshd_config

# sudo systemctl restart ssh
