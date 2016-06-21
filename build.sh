#!/usr/bin/env sh

###################################################
#Should be installed through git clone --recursive#
###################################################

######################################
#initialize triblers crap            #
#only works on ubuntu 14.04 and 16.04#
######################################

#allow for add-apt-repository

#apt-get install -y --force-yes software-properties-common python-software-properties

#ensure wxgtk2.8 and all requirements are available for 16.04, also twisted 15.x+
#add-apt-repository "deb http://archive.ubuntu.com/ubuntu vivid main"
#add-apt-repository "deb http://archive.ubuntu.com/ubuntu xenial main"


# update the apt-get folder.
apt-get update

# ensure python and pip are installed
apt-get install -y --force-yes python2.7
apt-get install -y --force-yes python-pip

#install other tribler requirements
sudo apt-get install -y --force-yes vlc libav-tools libjs-excanvas libjs-mootools libx11-6 python-apsw python-cherrypy3 python-crypto python-feedparser python-leveldb python-libtorrent python-m2crypto python-netifaces python-pil python-pyasn1 python-requests python-twisted python-wxgtk2.8 python-decorator python-gmpy gconf2 python-cffi python-enum34
pip install decorator==4.0.9

#install libsodium13 which does not exist anymore under 14.04
wget http://launchpadlibrarian.net/191505542/libsodium13_1.0.1-1_amd64.deb
dpkg -i libsodium13_1.0.1-1_amd64.deb


#install python-cryptography which does not exist anymore under 14.04
sudo apt-get install -y --force-yes python-cffi python-enum34
wget http://launchpadlibrarian.net/200479300/python-cryptography_0.8-1ubuntu2_amd64.deb
dpkg -i python-cryptography_0.8-1ubuntu2_amd64.deb

#install tribler itself
#pip install git+https://github.com/Tribler/tribler
pip install git+https://github.com/mitchellolsthoorn/tribler@feature/market

rm python-cryptography_0.8-1ubuntu2_amd64.deb
#rm tribler_6.5.2_all.deb
rm libsodium13_1.0.1-1_amd64.deb

###########################
#Install java for selenium#
###########################
apt-get install -y --force-yes gnome-terminal default-jre

##############################
#Install firefox for selenium#
##############################
#apt-get install -y --force-yes firefox=45.0.2+build1-0ubuntu1
apt-get install -y --force-yes firefox=28.0+build2-0ubuntu2

##################################################
#Install Xvfb to enable headless Firefox Selenium#
##################################################
sudo apt-get install -y --force-yes xorg xvfb xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic

###################################
#Install other python requirements#
###################################

pip install -r requirements.txt

pip install https://download.electrum.org/2.6.4/Electrum-2.6.4.tar.gz

#sh run.sh
