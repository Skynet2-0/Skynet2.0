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

    def __init__(self, hostip, user, password, port=None):
        """
        Constructs the Installer.

        hostip -- the ip address of the host.
        user -- the username of the user (Usually it will be host).
        password -- the password.
        port -- the port to connect to. (Default is None)
        """
        # self.ip = hostip
        # self.user = user
        # self.password = password
        self.ssh = SSH(hostip, user, password, port)

    def install(self):
        """
        Makes the class install itself through SSH.

        It also starts running the class.
        """
        print('Start installing.')
        (_, out0, err0) = self.ssh.run('apt-get update')
        self._checkStreams(out0, err0, 'apt update failed', 'apt updated.')
        (_, out0, err0) = self.ssh.run('apt-get install -y --force-yes git')
        self._checkStreams(out0, err0, 'git install failed', 'git installed.')
        command = 'git clone --recursive https://github.com/Skynet2-0/Skynet2.0.git'
        (_, out0, err0) = self.ssh.run(command)
        self._checkStreams(out0, err0, 'git clone failed', 'project cloned.')
        command = """cd Skynet2.0 && sh build.sh"""
        (_, out0, err0) = self.ssh.run(command)
        self._checkStreams(out0, err0, 'build failed', 'project build.')
        print('Installation finished.')

    def _checkStreams(self, out, err, errmessage='', succesmessage=None):
        """
        Checks the streams for error message and exit code.

        out -- the output stream.
        err -- the error stream.
        errmessage -- the message at the start after error. (Default is '')
        succesmessage -- the message on succes. (Default is None)
        """
        timeout = time.time() + 300 # Remember time 5 minutes from now to prevent infinite loops.
        done = False
        while time.time() <= timeout and not done:
            if out.channel.exit_status_ready():
                exitcode = out.channel.recv_exit_status()
                if exitcode != 0:
                    print("Error %s: %s\nexit status: %i" % (errmessage,
                                err.read().decode(), exitcode))
                elif succesmessage is not None:
                    print(succesmessage)
                done = True
            else:
                time.sleep(1)

    def finish(self):
        "Does some clean up."
        self.ssh.close_connection()
