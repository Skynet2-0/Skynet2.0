#!/usr/bin/env sh

###########################
#initialize the submodules#
###########################
git submodule add https://github.com/Tribler/tribler
git submodule add https://github.com/prusnak/addrgen
git submodule init --recursive /submodules
git submodule update --recursive /submodules

apt-get install python

#sh run.sh
