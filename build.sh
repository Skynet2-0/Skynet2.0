#!/usr/bin/env sh

###################################################
#Should be installed through git clone --recursive#
###################################################

######################################
#initialize triblers crap            #
#only works on ubuntu 14.04 and 16.04#
######################################

#ensure wxgtk2.8 and all requirements are available for 16.04
sudo add-apt-repository "deb http://archive.ubuntu.com/ubuntu vivid main"
sudo add-apt-repository "deb http://archive.ubuntu.com/ubuntu xenial main"

# update the apt-get folder.
sudo apt-get update

# ensure python and pip are installed
apt-get install -y python
apt-get install -y python-pip

#install libsodium13 which does not exist anymore under 14.04

wget http://launchpadlibrarian.net/191505542/libsodium13_1.0.1-1_amd64.deb
dpkg -i libsodium13_1.0.1-1_amd64.deb

#install python-cryptography which does not exist anymore under 14.04

wget http://launchpadlibrarian.net/200479300/python-cryptography_0.8-1ubuntu2_amd64.deb
dpkg -i python-cryptography_0.8-1ubuntu2_amd64.deb

#install other tribler requirements
sudo apt-get install -y libav-tools libjs-excanvas libjs-mootools libx11-6 python-apsw python-cherrypy3 python-crypto python-feedparser python-leveldb python-libtorrent python-m2crypto python-netifaces python-pil python-pyasn1 python-requests python-twisted python-wxgtk2.8 python2.7 vlc python-pip python-decorator python-gmpy gconf2 python-cffi python-enum34
pip install decorator==4.0.9

#install tribler itself
pip install git+https://github.com/Tribler/tribler

rm python-cryptography_0.8-1ubuntu2_amd64.deb
#rm tribler_6.5.2_all.deb
rm libsodium13_1.0.1-1_amd64.deb

###########################
#Install java for selenium#
###########################
apt-get install -y gnome-terminal default-jre

##############################
#Install firefox for selenium#
##############################
apt-get install -y firefox

###################################
#Install other python requirements#
###################################

pip install -r requirements.txt

#sh run.sh
