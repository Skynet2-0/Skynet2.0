FROM ubuntu:14.04
MAINTAINER Skynet2.0 <Skynet2dev@gmail.com>
RUN apt-get update && apt-get install -y git
RUN git clone --recursive https://github.com/Skynet2-0/Skynet2.0.git

#RUN /Users/parallels/Skynet2.0/build.sh

#############################################################
############## Fill in contents of build.sh #################
#############################################################

######################################
#initialize triblers crap            #
#only works on ubuntu 14.04 and 16.04#
######################################

#allow for add-apt-repository
RUN apt-get install -y software-properties-common python-software-properties

#ensure wxgtk2.8 and all requirements are available for 16.04, also twisted 15.x+
RUN add-apt-repository "deb http://archive.ubuntu.com/ubuntu vivid main"
RUN add-apt-repository "deb http://archive.ubuntu.com/ubuntu xenial main"

# Add universe for pip.
RUN apt-add-repository universe

# update the apt-get folder.
RUN apt-get update
# RUN apt-get upgrade -y

# ensure python and pip are installed
RUN apt-get install -y python
RUN apt-get install -y python-pip
# RUN apt-get install -y curl
# RUN curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py" && python get-pip.py && rm get-pip.py

#install other tribler requirements
# RUN apt-get install -y libldb1=1:1.1.24
# RUN apt-get install -y libldb1 libcups2 libnettle4 libhogweed2 samba-libs libgnutls28 libsmbclient vlc-nox libvlccore7
RUN apt-get install -y libav-tools libjs-excanvas libjs-mootools libx11-6 python-apsw
RUN apt-get install -y python-cherrypy3 python-crypto python-feedparser python-leveldb python-libtorrent python-m2crypto python-netifaces python-pil python-pyasn1 python-requests python-twisted python-wxgtk2.8 python2.7
RUN apt-get install -y python-decorator python-gmpy gconf2
RUN apt-get install -y python-cffi python-enum34
RUN apt-get install -y vlc
RUN pip install decorator==4.0.9

#install libsodium13 which does not exist anymore under 14.04
RUN wget http://launchpadlibrarian.net/191505542/libsodium13_1.0.1-1_amd64.deb
RUN dpkg -i libsodium13_1.0.1-1_amd64.deb

#install python-cryptography which does not exist anymore under 14.04
RUN wget http://launchpadlibrarian.net/200479300/python-cryptography_0.8-1ubuntu2_amd64.deb
RUN dpkg -i python-cryptography_0.8-1ubuntu2_amd64.deb

#install tribler itself
RUN pip install git+https://github.com/Tribler/tribler

RUN rm python-cryptography_0.8-1ubuntu2_amd64.deb
#RUN rm tribler_6.5.2_all.deb
RUN rm libsodium13_1.0.1-1_amd64.deb

###########################
#Install java for selenium#
###########################
RUN apt-get install -y gnome-terminal default-jre

##############################
#Install firefox for selenium#
##############################
RUN apt-get install -y firefox

###################################
#Install other python requirements#
###################################

RUN pip install -r requirements.txt

#sh run.sh

#############################################################
#################### End of build.sh ########################
#############################################################
