#!/usr/bin/env sh

pip3 install -r requirements.txt

PYTHONPATH=~/Skynet2.0/src python3 src/agent/agentCore.py

