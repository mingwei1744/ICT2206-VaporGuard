#!/bin/bash
# Script1. Server configurations

root="${rootUser}"
webadm="${webUser}"

timestamp=`date "+%Y-%m-%d %H:%M:%S"`
log="/home/$root/config.log"
touch $log

sudo apt update -y
#===================================================================#
# Create new user
#===================================================================#
sudo useradd $webadm
sudo usermod -aG sudo $webadm

if id $webadm >/dev/null 2>&1; then
  echo "$timestamp Created $webadm user" >> $log
else
  echo "$timestamp Failed to add user $webadm."
fi

#===================================================================#
# Configure firewall
# Commented out to keep port 22 as default SSH 
#===================================================================#
# sudo cp -a -v /etc/ssh/sshd_config /etc/ssh/sshd_config_backup
# sudo ufw limit ssh
# echo "y" | sudo ufw enable

# # Write configs to sshd_config
# sudo echo "
# PermitRootLogin no
# PasswordAuthentication no
# AllowUsers $root" >> /etc/ssh/sshd_config 

# # Configure SSH to run on port 1002
# sudo ufw limit 1002/tcp
# sudo echo "Port 1002" >> /etc/ssh/sshd_config

# sudo systemctl restart ssh
