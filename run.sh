#!/usr/bin/env sh

###########################
#Start the selenium server#
###########################
nohup java -jar selenium-server-standalone-2.53.0.jar &


#################
#Start the agent#
#################
PYTHONPATH=${PYTHONPATH}:. python agent/agentCore.py
