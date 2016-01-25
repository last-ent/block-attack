#!/usr/bin/env bash

sudo add-apt-repository ppa:fkrull/deadsnakes # Provides access to Py 3.5
sudo aptitude update
sudo aptitude upgrade

sudo aptitude install -y python3.5-dev
sudo aptitude install -y nginx=1.9.2
sudo aptitude install -y python-virtualenv
virtualenv /home/vagrant/henv --python=python3.5
sudo aptitude install -y supervisor
/home/vagrant/henv/bin/pip install -r /var/www/http/pip_requirements.txt

# Redis Setup
wget http://download.redis.io/redis-stable.tar.gz /home/vagrant/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd /home/vagrant/redis-stable
make
sudo make install
cd utils
# sudo ./install_server.sh ## This step requires us to enter port in shell. So better do this manually.