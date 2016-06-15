#! /usr/bin/env python

"""
This script will start the tribler exit node.

It will then occasionally check it's wallet.
and if it's wallet has enough money it will procure, install and start exactly 1 child.

It's reproductive strategy will be to create a child, transfer all it's bitcoin to the child.
At most it will make 1 child.
It will log all output of the child.
"""
from ExitNode import Tunnel
from Birthchamber import Birthchamber
from ZappiehostBuyer import ZappiehostBuyer
from Wallet import Wallet
from time import sleep
from Tribler.community.tunnel.tunnel_community import TunnelSettings
from twisted.internet.stdio import StandardIO

wallet = Wallet()

settings = TunnelSettings()

# For disabling anonymous downloading, limiting download to hidden services only
settings.min_circuits = 0
settings.max_circuits = 0
settings.become_exitnode = True
crawl_keypair_filename = None
dispersy_port = -1

tunnel = Tunnel(settings, crawl_keypair_filename, dispersy_port)
#StandardIO(LineHandler(tunnel, profile))
tunnel.start(None)



print("successful instantiation")

#prepare the possibility to get a child
bc = Birthchamber()

#this should actually compare with the current necessary bitcoins plus a small margin
while(wallet.balance()<bc.getChildCost()):
    print("Not enough bitcoins, waiting for money to arrive")
    sleep(600)

bc.getChild()

#get the wallet address of the child
f = open("python.log", "r")
fr = f.read()
