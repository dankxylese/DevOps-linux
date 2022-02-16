#!/bin/bash
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install nginx -y
sudo apt-get install npm -y
sudo apt-get install python-software-properties

#Add database env var early on
#echo "export DB_HOST='mongodb://192.168.56.5:27017/posts'" >> ~/.bashrc
#Tell system to refresh bashrc cache
#source ~/.bashrc

curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
sudo apt-get install nodejs -y
sudo npm install pm2 -g

#install forever and app
cd ~/code/app
#sudo npm install forever -g
npm install

#set up port forwarding
sudo cp ~/code/default /etc/nginx/sites-available/
sudo systemctl restart nginx

#start the app for the first time
forever start app.js

#make it start automatically when you boot after first setup
# HAVE to make this run as vagrant user instead of root which is default, for it to even work
#(crontab -l 2>/dev/null; echo "@reboot sleep 10 && sh /home/vagrant/code/app/startForever.sh") | crontab -
