#!/usr/bin/bash
 
export IMAGE_GALLERY_SCRIPT_VERSION="1.0"

# Install Packages
yum -y update
yum install -y python3 git

# Configure/Install Custom Software
cd /home/ec2-user
git clone https://github.com/dairazuaje/python-image-gallery.git
chown -R ec2-user:ec2-user python-image-gallery
cd ~/python-image-gallery
su ec2-user -l -c "cd ~/python-image-gallery && pip3 install -r requirements.txt --user"

# Start/Enable Services
sudo systemctl stop postfix
sudo systemctl disable postfix

su ec2-user -l -c "cd ~/python-image-gallery && ./start">/var/log/image_gallery.log 2>&1 &


