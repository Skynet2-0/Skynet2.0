import xmlrpclib

class Client(object):
    """"""

    def __init__(self, ip, port):
        """
        The client for the rpc.

        ip -- The ip address or host to connect to.
        port -- The port number.
        """
        host = 'http://%s:%s' % (ip, str(port))
        self.server = xmlrpclib.ServerProxy(host)

    def list_functions(self):
        self.server.system.listMethods()

    @property
    def server(self):
        """The server to use."""
        return self._server

    @server.setter
    def server(self, server):
        self._server = server

    def add(self, wallet):
        """
        Adds this client to the servers.

        wallet -- The wallet address used.
        """
        from DNA import DNA
        from CountryGetter import CountryGetter
        import ipgetter
        dna = DNA().json
        ip = ipgetter.myip()
        country = CountryGetter.get_country()
        self.server.add(ip, wallet, country, dna)

c = Client('localhost', 8000)
c.add("A wallet address")
print(c.server.list_files())
c.server.remove()
print(c.server.list_files())

"""
# Code for testing the rpc.
c = Client('localhost', 8000)
c.server.add('127.0.0.1', 'A wallet address', 'Netherlands', {"vps buyers": {"ThcserversBuyer": 0.25, "OffshoredediBuyer": 0.25, "ZappiehostBuyer": 0.25, "SharkserversBuyer": 0.25}, "mutate rate": 0.05, "own vps": "ZappiehostBuyer"})
print(c.list_functions())
c.server.update('127.0.0.1', '100')
print(c.server.list_files())
c.server.remove()
print(c.server.list_files())
"""
