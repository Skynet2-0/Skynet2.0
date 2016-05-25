# You can run this .tac file directly with:
#    twistd -y file

"""
This .tac file will start a twistd session with a tribler service added that runs with multichain and exitnode enabled
"""

import os
from twisted.application import service, internet
from twisted.web import static, server
from twisted.python.logfile import DailyLogFile
from twisted.python.log import ILogObserver, FileLogObserver
from tribler_plugin import TriblerServiceMaker

def getTriblerService():
    """
    Return a service suitable for creating an application object.

    This service is a headless tribler instance with exit node and multichain enabled
    """
    tsm = TriblerServiceMaker()
    return tsm.makeService({'manhole': None})
    
    # create a resource to serve static files
    #fileServer = server.Site(static.File(os.getcwd()))
    #return internet.TCPServer(8080, fileServer)

# this is the core part of any tac file, the creation of the root-level
# application object
# it creates 
application = service.Application("Tribler application")
logfile = DailyLogFile("tribler.log", "/tmp")
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)

# attach the service to its parent application
service = getTriblerService()
service.setServiceParent(application)
