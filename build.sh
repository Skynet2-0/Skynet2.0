###########################
#initialize the submodules#
###########################
git submodule add https://github.com/Tribler/tribler
git submodule add https://github.com/prusnak/addrgen
git submodule init --recursive /submodules
git submodule update --recursive /submodules

apt-get install python3
apt-get install pip3

#sh run.sh
