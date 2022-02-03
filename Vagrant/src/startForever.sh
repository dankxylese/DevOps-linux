#!/bin/bash
cd /home/vagrant/code/app/
node seeds/seed.js
forever start app.js
echo "STARTED RUNNING FOREVER"
