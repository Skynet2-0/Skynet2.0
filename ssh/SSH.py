"""
Created on Apr 29, 2016

@author: Stefan
"""
from paramiko.client import *
import paramiko
import time
from Settings import Settings


class SSH(object):
    """
    This class enables the execution of SSH commands on a child server.

    It works by wrapping the paramiko client class.
    """

    default_use_logfile = False

    def __init__(self, sshhost, username, pwd, port=None, use_log=False):
        """
        Constructor for the SSH class.

        This constructor connects automatically to sshhost over ssh so manual
        calling of the connect function is not necessary.

        sshhost -- the host to connect to.
        username -- the username to use.
        pwd -- the password.
        port -- the port to connect to.
        use_log -- Whether to log the ssh connection in a logfile. (Default is False)
        """
        self.sshhost = sshhost
        self.username = username
        self.pwd = pwd
        self.client = SSHClient()
        # only activate when non-agent, as this will throw unhandled prompts
        # self.client.set_missing_host_key_policy(WarningPolicy())
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.load_system_host_keys()
        self.connect(port=port)
        
        s = Settings()
        if s.enable_global_ssh_logging:
            self.use_logfile(True)
        else:
            self.use_logfile(use_log)

    def connect(self, sshhost = None, user = None, pwd = None, port = None):
        """
        Connects this instance with the instance sshhost over SSH.

        username -- the user and pwd is the password.
        Port -- the port number to connect to.
        See SSHClient.connect for more information on optional parameters
        that can be set when using the underlying layer instead of this one.
        """
        if sshhost is None:
            sshhost = self.sshhost
        if user is None:
            user = self.username
        if pwd is None:
            pwd = self.pwd
        if port is not None:
            self.client.connect(sshhost, username = user, password = pwd, port=port)
        else:
            self.client.connect(sshhost, username = user, password = pwd)

    def run(self, command):
        """
        Runs a command over SSH on the client.

        command -- the command to execute.
        Return a tuple of the stdin, stdout, and stderr of the executing command,
        as a 3-tuple.
        """
        (ins, out, err) = self.client.exec_command(command)
        if self.use_log:
            with open("Skynet.log", 'a') as file:
                file.write("executing command: %s\n" % command)
                file.write("%s\n" % out.read().decode())
                file.write("%s\n" % err.read().decode())
                file.write("Exit status: %i\n\n" % out.channel.recv_exit_status())
        return (ins, out, err)

    def close_connection(self):
        """
        Closes the SSH connection between this and the client.
        """
        self.client.close()

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

    def use_logfile(self, use_log=True):
        """
        Sets whether or not to use a logfile

        use_log -- Whether to use a logfile. (Default is False)
        """
        assert type(use_log) == bool
        self.use_log = use_log

    