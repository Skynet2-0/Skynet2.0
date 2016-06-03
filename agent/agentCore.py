#! /usr/bin/env python

"""
This script will start the tribler exit node.

It will then occasionally check it's wallet.
and if it's wallet has enough money it will procure, install and start exactly 1 child.

It's reproductive strategy will be to create a child, transfer all it's bitcoin to the child.
At most it will make 1 child.
It will log all output of the child.
"""

from ExitNode import ExitNode
from Birthchamber import Birthchamber
from Wallet import Wallet
from time import sleep
from ssh.SSH import SSH


SSH.global_use_logfile()

en = ExitNode()

wallet = Wallet()

print("successful instantiation")

#prepare the possibility to get a child
bc = Birthchamber()

#this should actually compare with the current necessary bitcoins plus a small margin
while(wallet.balance()<bc.getChildPrice()):
    print("Not enough bitcoins, waiting for money to arrive")
	sleep(600)

bc.getChild(ZappiehostBuyer())