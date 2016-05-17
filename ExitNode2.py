"""
This twistd plugin enables to start Tribler headless using the twistd command.
Starts the program with exitnode and multichain enabled. heavily based on tribler\twisted\twisted\plugins\tribler_plugin
"""
import logging
import os
import signal
from time import sleep

from twisted.application.service import MultiService, IServiceMaker
from twisted.conch import manhole_tap
from twisted.internet import reactor
from twisted.plugin import IPlugin
from twisted.python import usage
from twisted.python.log import msg
from zope.interface import implements

from Tribler.Core.Modules.process_checker import ProcessChecker
from Tribler.Core.Session import Session
from Tribler.Core.SessionConfig import SessionStartupConfig


class Options(usage.Options):
    optParameters = [
        ["manhole", "m", 0, "Enable manhole telnet service listening at the specified port", int],
    ]


class TriblerServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = "tribler_exit_node"
    description = "Tribler exit node twistd plugin, starts Tribler exit node as a service"
    options = Options

    def __init__(self):
        """
        Initialize the variables of the TriblerServiceMaker and the logger.
        """
        self.session = None
        self._stopping = False

    def shutdown_process(self, shutdown_message, code=1):
        msg(shutdown_message)
        reactor.addSystemEventTrigger('after', 'shutdown', os._exit, code)
        reactor.stop()

    def start_tribler(self):
        """
        Main method to startup Tribler.
        """

        def signal_handler(sig, _):
            msg("Received shut down signal %s" % sig)
            if not self._stopping:
                self._stopping = True
                self.session.shutdown()
                msg("Tribler shut down")
                reactor.stop()
                self.process_checker.remove_lock_file()
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        config = SessionStartupConfig()
		config.set_torrent_checking(False)
        config.set_multicast_local_peer_discovery(False)
        config.set_megacache(False)
        config.set_dispersy(True)
        config.set_mainline_dht(True)
        config.set_torrent_collecting(False)
        config.set_libtorrent(True)
        config.set_dht_torrent_collecting(False)
        config.set_enable_torrent_search(False)
        config.set_videoplayer(False)
        #config.set_dispersy_port(self.dispersy_port)
        config.set_enable_torrent_search(False)
        config.set_enable_channel_search(False)
		config.set_enable_multichain(True)		
		config.set_tunnel_community_exitnode_enabled(True)
		

        # Check if we are already running a Tribler instance
        self.process_checker = ProcessChecker()
        if self.process_checker.already_running:
            self.shutdown_process("Another Tribler instance is already using statedir %s" % config.get_state_dir())
            return

        msg("Starting Tribler")

        self.session = Session(config)
        upgrader = self.session.prestart()
        if upgrader.failed:
            self.shutdown_process("The upgrader failed: .Tribler directory backed up, aborting")
        else:
            self.session.start()
            msg("Tribler Exit Node started")

    def makeService(self, options):
        """
        Construct a Tribler service.
        """
        tribler_service = MultiService()
        tribler_service.setName("Tribler_ExitNode")

        '''manhole_namespace = {}
        if options["manhole"]:
            port = options["manhole"]
            manhole = manhole_tap.makeService({
                'namespace': manhole_namespace,
                'telnetPort': 'tcp:%d:interface=127.0.0.1' % port,
                'sshPort': None,
                'passwd': os.path.join(os.path.dirname(__file__), 'passwd'),
            })
            tribler_service.addService(manhole)'''

        reactor.callWhenRunning(self.start_tribler)

        return tribler_service

service_maker = TriblerServiceMaker()