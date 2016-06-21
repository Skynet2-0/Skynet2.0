import xmlrpclib

class Client(object):
    """The client of the rpc."""

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
        from agent.DNA import DNA
        from agent.CountryGetter import CountryGetter
        import ipgetter
        dna = DNA().json
        ip = ipgetter.myip()
        country = CountryGetter.get_country()
        self.server.add(ip, wallet, country, dna)

    def update_upload(self):
        """Updates the upload capacity."""
        regex = "[A-z0-9]+:(?:\W+[0-9]+){8}\W+([0-9]+)"
        import ipgetter
        import re
        ip = ipgetter.myip()
        filename = "/proc/net/dev"
        read = None
        with open(filename, "r") as f:
            read = f.read()
        if read is not None:
            matches = re.findall(regex, read)
            print("%s matches found." % str(len(matches)))
            total = 0L
            for upload in matches:
                total += long(upload)
                print('total is: %s' % str(total))
            self.server.update(ip, str(upload))
        else:
            print("Read of %s failed to produce any matches." % filename)

"""
# Code for testing the rpc.
c = Client('localhost', 8000)
c.server.add('127.0.0.1', 'A wallet address', 'Netherlands', {"vps buyers": {"ThcserversBuyer": 0.25, "OffshoredediBuyer": 0.25, "ZappiehostBuyer": 0.25, "SharkserversBuyer": 0.25}, "mutate rate": 0.05, "own vps": "ZappiehostBuyer"})
print(c.list_functions())
c.server.update('127.0.0.1', '100')
print(c.server.list_files())
c.server.remove()
print(c.server.list_files())


c = Client('localhost', 8000)
c.add('A wallet address')
c.update_upload()
print(c.server.list_files())
c.server.remove()
print(c.server.list_files())
"""
