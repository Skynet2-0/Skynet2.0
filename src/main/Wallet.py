"""
Created on April 20, 2016.

@author: Stefan
"""

import bitcoinrpc


class Wallet(object):
    """This class enables bitcoin transactions."""

    def __init__(self):
        """Initialize the bitcoin wallet."""
        self.connection = bitcoinrpc.connect_to_local()
        self.address = self.connection.getnewaddress()

    def __init__(self, address):
        """
        Initialize the bitcoin wallet with the given address.
        address is the address to use.
        """
        self.connection = bitcoinrpc.connect_to_local()
        self.address = address

    def __init__(self, address, connection):
        """
        Initialize the bitcoin wallet with the given address.
        This version is used for testing purposes.
        address is the address to use.
        connection is the connection to use.
        """
        self.connection = connection
        self.address = address

    def getSaldo(self):
        """Checks the saldo of the wallet."""
        self.connection.getBalance()

    def getAddress(self):
        """This method gets the wallets address."""
        return self.address

    def transfer(self, amount, recipient):
        """
        Transfers amount money from self to the recipient.
        Returns True iff the method to transfer is called.
        Returns False iff the address of the recipient is invalid.
        """
        valid = self.validateaddress(recipient)
        if valid.isvalid():
            self.send_to_address(recipient, amount)
            return True
        else:
            return False
