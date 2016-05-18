#!/usr/bin/env sh

###########################
#Start the selenium server#
###########################
nohup java -jar selenium-server-standalone-2.53.0.jar &


#################
#Start the agent#
#################
nohup PYTHONPATH=~/Skynet2.0 python src/agent/agentCore.py &
