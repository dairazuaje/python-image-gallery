#!/usr/bin/bash                                                                                                                                                                                                                      

export IMAGE_GALLERY_SCRIPT_VERSION="1.1"
CONFIG_BUCKET="edu.au.cc.image-gallery-config-dza0042"

# Install Packages                                                                                                                                                                                                                  
yum -y update
yum install -y python3 git postgresql postgresql-devel gcc python3-devel
amazon-linux-extras install -y nginx1

# Configure/Install Custom Software                                                                                                                                                                                                 cd /home/ec2-user
git clone https://github.com/dairazuaje/python-image-gallery.git
chown -R ec2-user:ec2-user python-image-gallery
cd ~/python-image-gallery
su ec2-user -l -c "cd ~/python-image-gallery && pip3 install -r requirements.txt --user"

aws s3 cp s3://${CONFIG_BUCKET}/nginx/nginx.conf /etc/nginx
aws s3 cp s3://${CONFIG_BUCKET}/nginx/default.d/image_gallery.conf /etc/nginx/default.d

# Start/Enable Services                                                                                                                                                                                                             
systemctl stop postfix
systemctl disable postfix
systemctl start nginx
systemctl enable nginx

su ec2-user -l -c "cd ~/python-image-gallery && ./start">/var/log/image_gallery.log 2>&1 & 
