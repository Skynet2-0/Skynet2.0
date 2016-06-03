"""
This class can start a child once it has been installed unto.
"""

from SSH import SSH
from abc import *


class AbstractStarter(object):
    """Abstract class that arranges the starting up of the server."""
    __metaclass__ = ABCMeta

    def __init__(self, hostip, user, password, port=None, use_log=None):
        """
        Constructs the Starter which starts the program.

        hostip -- the ip address of the host.
        user -- the username of the user (Usually it will be host).
        password -- the password.
        port -- the port to connect to. (Default is None)
        use_log -- True for logging the starting. (Default is None)
        """
        if (use_log is None):
            self.ssh = SSH(hostip, user, password, port)
        else:
            self.ssh = SSH(hostip, user, password, port, use_log)

    @abstractmethod
    def start(self):
        """ Starts the program. """
        pass
        #self._checkStreams(out0, err0, 'apt update failed', 'apt updated.')

    def finish(self):
        """Does some clean up for the class."""
        self.ssh.close_connection()

class Starter(AbstractStarter):
    """
    This class is responsable for sending the startup commands to
    the child server. It uses the SSH class to send them.
    """

    def __init__(self, hostip, user, password, port=None, use_log=None):
        """
        Constructs the Starter which starts the program.

        hostip -- the ip address of the host.
        user -- the username of the user (Usually it will be host).
        password -- the password.
        port -- the port to connect to. (Default is None)
        use_log -- True for logging the starting. (Default is None)
        """
        super(Starter, self).__init__(hostip, user, password, port, use_log)

    def start(self):
        """ Starts the program. """
        (_, out0, err0) = self.ssh.run('sh run.sh')
        #self._checkStreams(out0, err0, 'apt update failed', 'apt updated.')

class DockerStarter(AbstractStarter):
    """Starts up the project using docker."""

    def __init__(self, hostip, user, password, port=None, use_log=None):
        """
        Constructs the Starter which starts the program.

        hostip -- the ip address of the host.
        user -- the username of the user (Usually it will be host).
        password -- the password.
        port -- the port to connect to. (Default is None)
        use_log -- True for logging the starting. (Default is None)
        """
        super(DockerStarter, self).__init__(hostip, user, password, port, use_log)

    def start(self):
        """Starts the program."""
        (_, out, err) = self.ssh.run('docker -t -i root/ubuntu:Skynet2.0 /bin/bash')
        self.ssh._checkStreams(out, err, 'Container creation failed', 'Succesfully created container.')
        (_, out, err) = self.ssh.run('cd Skynet2.0 && sh run.sh')
        self.ssh._checkStreams(out, err, 'Program did not start', 'Program started.')
