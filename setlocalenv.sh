#!/bin/bash
#If there is no python virtualenv on your local enviroment then run this script.i  
sudo apt-get install -y python-pip
sudo pip install  virtualenv virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
#Change it to your local work directory.
export PROJECT_HOME=$HOME/workspace     
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv pythonstudy
#workon pythonstudy
sudo apt-get -y install python-dev libjpeg-dev libfreetype6-dev zlib1g-dev 
sudo apt-get -y install python-imaging
sudo apt-get -y install pbr
