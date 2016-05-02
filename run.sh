#!/usr/bin/env sh

pip install -r requirements.txt

PYTHONPATH=.:./src python src/agent/agentCore.py
