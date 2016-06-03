"""
Created on May 2, 2016.

@author: Stefan
"""
from SSH import SSH
import time
from abc import *


class AbstractInstaller(object):
    """
    Abstract class that facilitates installation of child servers.

    The SSH class is used to send the commands.
    """
    __metaclass__ = ABCMeta

    def __init__(self, hostip, user, password, port=None, use_log=None):
        """
        Constructs the Installer.

        hostip -- the ip address of the host.
        user -- the username of the user (Usually it will be host).
        password -- the password.
        port -- the port to connect to. (Default is None)
        use_log -- True for logging the installation. (Default is None)
        """
        if (use_log is None):
            self.ssh = SSH(hostip, user, password, port)
        else:
            self.ssh = SSH(hostip, user, password, port, use_log)

    @abstractmethod
    def install(self):
        """Makes the class install itself through SSH."""
        pass

    def finish(self):
        "Does some clean up."
        self.ssh.close_connection()

class Installer(AbstractInstaller):
    """
    This class is responsable for sending the install commands to the child
    server.

    It uses the SSH class to send them.
    """

    def __init__(self, hostip, user, password, port=None, use_log=None):
        """
        Constructs the Installer.

        hostip -- the ip address of the host.
        user -- the username of the user (Usually it will be host).
        password -- the password.
        port -- the port to connect to. (Default is None)
        use_log -- True for logging the installation. (Default is None)
        """
        super(Installer, self).__init__(hostip, user, password, port, use_log)

    def install(self):
        """Makes the project install itself through SSH."""
        print('Start installing.')
        (_, out0, err0) = self.ssh.run('apt-get update')
        self.ssh._checkStreams(out0, err0, 'apt update failed', 'apt updated.')
        (_, out0, err0) = self.ssh.run('apt-get install -y git')
        self.ssh._checkStreams(out0, err0, 'git install failed', 'git installed.')
        command = 'git clone --recursive https://github.com/Skynet2-0/Skynet2.0.git'
        (_, out0, err0) = self.ssh.run(command)
        self.ssh._checkStreams(out0, err0, 'git clone failed', 'project cloned.')
        command = """cd Skynet2.0 && sh build.sh"""
        (_, out0, err0) = self.ssh.run(command)
        self.ssh._checkStreams(out0, err0, 'build failed', 'project build.')
        print('Installation finished.')

    class DockerInstaller(AbstractInstaller):
        """
        This class aranges the installation through the docker class.
        """

        def __init__(self, hostip, user, password, port=None, use_log=None):
            """
            Constructs the Installer.

            hostip -- the ip address of the host.
            user -- the username of the user (Usually it will be host).
            password -- the password.
            port -- the port to connect to. (Default is None)
            use_log -- True for logging the installation. (Default is None)
            """
            super(DockerInstaller, self).__init__(hostip, user, password, port, use_log)

        def install(self):
            """Makes the project """
            (_, out, err) = self.ssh.run('apt-get install -y curl')
            self.ssh._checkStreams(out, err, 'Installing curl failed', 'curl installed')
            (_, out, err) = self.ssh.run('curl -fsSL https://get.docker.com/gpg | apt-key add -')
            self.ssh._checkStreams(out, err, 'Adding docker key failed', 'Docker key added')
            (_, out, err) = self.ssh.run('curl -fsSL https://get.docker.com/ | sh')
            self.ssh._checkStreams(out, err, 'Installing docker failed', 'Docker installed')
            (_, out, err) = self.ssh.run('') # Load the image.
            self.ssh._checkStreams(out, err, 'Failed loading image', 'Docker image loaded')
