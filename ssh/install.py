"""
Created on May 2, 2016.

@author: Stefan
"""
from SSH import SSH
import time


class Installer(object):
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
        # self.ip = hostip
        # self.user = user
        # self.password = password
        if (use_log is None):
            self.ssh = SSH(hostip, user, password, port)
        else:
            self.ssh = SSH(hostip, user, password, port, use_log)

    def install(self):
        """
        Makes the class install itself through SSH.

        It also starts running the class.
        """
        print('Start installing.')
        (_, out0, err0) = self.ssh.run('apt-get update')
        self.ssh._checkStreams(out0, err0, 'apt update failed', 'apt updated.')
        (_, out0, err0) = self.ssh.run('apt-get install -y --force-yes git')
        self.ssh._checkStreams(out0, err0, 'git install failed', 'git installed.')
        command = 'git clone --recursive https://github.com/Skynet2-0/Skynet2.0.git'
        (_, out0, err0) = self.ssh.run(command)
        self.ssh._checkStreams(out0, err0, 'git clone failed', 'project cloned.')
        command = """cd Skynet2.0 && sh build.sh &> build.out"""
        (_, out0, err0) = self.ssh.run(command)
        self.ssh._checkStreams(out0, err0, 'build failed', 'project build.')
        print('Installation finished.')

    def finish(self):
        "Does some clean up."
        self.ssh.close_connection()
