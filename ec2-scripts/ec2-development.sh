#!/usr/bin/bash

# Install Packages
yum -y update
yum install -y emacs-nox nano tree python3
yum install -y git
amazon-linux-extras install -y nginx1
yum install -y gcc
yum install -y python3-devel
yum install -y postgresql-devel

# Configure/Install Custom Software
# Python Stuff
cd /home/ec2-user
git clone https://github.com/dairazuaje/python-image-gallery.git
chown -R ec2-user:ec2-user python-image-gallery
cd ~/python-image-gallery
su ec2-user -c "cd ~/python-image-gallery && pip3 install -r requirements.txt --user"

# Start/Enable Services
sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl stop postfix
sudo systemctl disable postfix
