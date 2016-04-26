"""
Created on April 20, 2016.

@author: Stefan
"""

import bitcoinrpc


class Wallet(object):
    """This class enables bitcoin transactions."""

    def __init__(self, address = None, config = None):
        """
        Initialize the bitcoin wallet.
        address is the address to use.
        connection is the connection to use. Setting the connection is
        useful for testing purposes or high control.
        """
        self.connection = bitcoinrpc.connect_to_local(config)
        if address is None:
            self.address = self.connection.getnewaddress()
        else:
            self.address = address

    def getSaldo(self):
        """Checks the saldo of the wallet."""
        self.connection.getbalance()

    def getAddress(self):
        """This method gets the wallets address."""
        return self.address

    def transfer(self, amount, recipient):
        """
        Transfers amount money from self to the recipient.
        Returns True iff the method to transfer is called.
        Returns False iff the address of the recipient is invalid.
        """
        valid = self.connection.validateaddress(recipient)
        if valid.isvalid():
            self.connection.send_to_address(recipient, amount)
            return True
        else:
            return False
