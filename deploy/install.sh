#!/bin/bash

# install ansible
sudo apt-add-repository -y ppa:ansible/ansible
sudo apt-get update
sudo apt-get install -y ansible git

# install dokku
wget https://raw.githubusercontent.com/dokku/dokku/master/bootstrap.sh
sudo bash bootstrap.sh