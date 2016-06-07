#!/usr/bin/env sh

####################################################
#Start Xvfb display simulation on display number 99#
####################################################
nohup Xvfb :99 -ac &
export DISPLAY=:99 &

###########################
#Start the selenium server#
###########################
nohup java -jar selenium-server-standalone-2.53.0.jar &


#################
#Start the agent#
#################
nohup agent/agentCore.py &
echo "started up the agent on this server"
