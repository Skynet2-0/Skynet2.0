"""
Created on April 20, 2016.

@author: Stefan
"""


class Wallet(object):
    """This class enables bitcoin transactions."""

    def __init__(self):
        """Initialize the bitcoin wallet"""
        self.connection = bitcoinrpc.connect_to_local()

    def getSaldo(self):
        """Checks the saldo of the wallet"""
        self.connection.getBalance()

    def getAddress(self):
        """This method gets the wallets address."""
        pass

    def transfer(self, amount, recipient):
        """Transfers amount money from self to the recipient"""
        self.send_to_address(recipient, amount)
