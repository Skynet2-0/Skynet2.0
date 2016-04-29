#!/usr/bin/env sh

pip3 install -r requirements.txt

PYTHONPATH=.:./src python3 src/agent/agentCore.py
