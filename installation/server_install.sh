#!/bin/bash

# ******************************************
# Initial setup and dependency installation
# ******************************************

# Check for root privileges
if [ "$EUID" -ne 0 ]
  then echo "PLEASE RUN THIS SCRIPT WITH ROOT PRIVILEGES"
  exit
fi

# Install required packages
apt update
apt install nginx ufw snapd

# Copy config files
cp cfg_files/nginx.conf /etc/nginx/
cp cfg_files/RSLLeaderboard /etc/nginx/sites-available/

# Install certbot and set of SSL certificates
snap install --classic certbot
ln -s /snap/bin/certbot /usr/bin/certbot

# Generating certificate should be done manually
# sudo certbot certonly --nginx
# Verify SSL certificate autorenewal
# sudo certbot renew --dry-run
# Double check cronjob exists
# systemctl list-timers

sudo nginx -t
sudo systemctl restart nginx

# Configure firewall
ufw allow ssh
ufw allow http
ufw allow https
ufw enable

# Set up the website directory
mkdir -p /var/www/RSLLeaderboard
chown -R www-data:www-data *

# Set up the backend as a system process
cp cfg_files/RSLLeaderboard.service /etc/systemd/system/
systemctl start RSLLeaderboard
systemctl enable RSLLeaderboard