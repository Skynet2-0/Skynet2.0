'''
This script will start the tribler exit node
It will then occasionally check it's wallet
and if it's wallet has enough money it will procure, install and start exactly 1 child
'''

from ExitNode import ExitNode
from src.agent.Birthchamber import Birthchamber
from src.agent.Wallet import Wallet
from time import sleep

#en = ExitNode()

wallet = Wallet()

#this should actually compare with the current necessary bitcoins plus a small margin
while(wallet.balance()<0.01):
	sleep(600)

bc = Birthchamber()
bc.getChild()
	