#!/usr/bin/env sh

######################################
#initialize triblers crap            #
#only works on ubuntu 14.04 and 16.04#
######################################

#ensure wxgtk2.8 and all requirements are available for 16.04
sudo add-apt-repository "deb http://archive.ubuntu.com/ubuntu vivid main"
sudo apt-get update

#install libsodium13 which does not exist anymore under 14.04
rm libsodium13_1.0.1-1_amd64.deb
wget http://launchpadlibrarian.net/191505542/libsodium13_1.0.1-1_amd64.deb
dpkg -i libsodium13_1.0.1-1_amd64.deb

#install python-cryptography which does not exist anymore under 14.04
rm python-cryptography_0.8-1ubuntu2_amd64.deb
wget http://launchpadlibrarian.net/200479300/python-cryptography_0.8-1ubuntu2_amd64.deb
dpkg -i python-cryptography_0.8-1ubuntu2_amd64.deb

#install other tribler requirements
sudo apt-get install libav-tools libjs-excanvas libjs-mootools libx11-6 python-apsw python-cherrypy3 python-crypto python-feedparser python-leveldb python-libtorrent python-m2crypto python-netifaces python-pil python-pyasn1 python-requests python-twisted python-wxgtk2.8 python2.7 vlc python-pip python-decorator python-gmpy gconf2
pip install decorator

#install tribler itself
rm tribler_6.5.1_all.deb
wget https://github.com/Tribler/tribler/releases/download/v6.5.1/tribler_6.5.1_all.deb
dpkg -i tribler_6.5.1_all.deb
apt-get install


###########################
#initialize the submodules#
###########################
#git submodule add https://github.com/Tribler/tribler
#git submodule add https://github.com/prusnak/addrgen
#git submodule init --recursive 
#git submodule update --recursive 

#sh run.sh
