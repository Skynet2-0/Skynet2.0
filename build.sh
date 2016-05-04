#!/usr/bin/env sh

###########################
#initialize the submodules#
###########################
git submodule add https://github.com/Tribler/tribler
git submodule add https://github.com/prusnak/addrgen
#git submodule init --recursive /submodules
#git submodule update --recursive /submodules

# update the apt-get folder.
apt-get update

apt-get install -y python3
#apt-get install -y pip3

# Necessities only available through apt-get
#apt-get install -y firefox

#sh run.sh
