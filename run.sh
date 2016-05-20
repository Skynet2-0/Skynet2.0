#!/usr/bin/env sh

###########################
#Start the selenium server#
###########################
nohup java -jar selenium-server-standalone-2.53.0.jar &


#################
#Start the agent#
#################
nohup python src/agent/agentCore.py &
