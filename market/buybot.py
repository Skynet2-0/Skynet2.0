"""
This file arranges the API for the market.

Created June 6, 2016.

@author: Stefan
"""

from agent.Wallet import Wallet
import agent.ExitNode
from market import Market
import time
from typing.typecheck import *


class AutoBuyBot(object):
    """This class arranges the buyer."""

    def __init__(self, market=None, wallet=None):
        """"""
        if market is None:
            self.market = self._initialize_market_if_none()
        else:
            check_type(market, Market)
            self.market = market
        if wallet is None:
            self.wallet = Wallet()
        else:
            self.wallet = wallet

    def _initialize_market_if_none(self):
        """
        Initializes the market if None was provided.
        """
        from twisted.internet.threads import blockingCallFromThread
        from Tribler.Core.Utilities.twisted_thread import reactor
        from Tribler.community.multichain.community import MultiChainCommunity, MultiChainCommunityCrawler
        from Tribler.community.market.community import MarketCommunity
        community = blockingCallFromThread(reactor, Exitnode.start_tribler.start_multichain_community)
        community = blockingCallFromThread(reactor, Exitnode.start_tribler.start_market_community)
        return Market(community)

    def run(self):
        """
        Runs the auto buy bot until there are no funds left.

        returns -- True upon succes.
        """
        amount = 0.01 # Approximately 10 kB.
        result = self._run(amount)
        print("Out of funds")
        return result

    def _run(self, amount, sleeptime=10):
        """
        Does the same as run.

        amount -- The amount to buy at a time.
        sleeptime -- The time to sleep. (Default is 10)
        """
        order = None
        while self.wallet.balance() >= 0:
            if order is None:
                order = self.market.buy(amount)
            elif not order.is_valid():
                order = None
            time.sleep(sleeptime)
        return True

    @property
    def market(self):
        """The market to buy on."""
        return self._market

    @market.setter
    def market(self, newmarket):
        self._market = newmarket

def main(argv):
    """The main thing."""
    buyer = AutoBuyBot()
    buyer.run()
