'''
Created on Apr 29, 2016

@author: Stefan
'''
from paramiko.client import *
import time

class SSH(object):
    '''
    This class enables the execution of SSH commands on a child server
    '''

    def __init__(self, sshhost, username, pwd, port = None):
        '''
        Constructor
        '''
        self.sshhost = sshhost
        self.username = username
        self.pwd = pwd
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(WarningPolicy())
        self.client.load_system_host_keys()
        self.connect(port=port)

    def connect(self, sshhost = None, user = None, pwd = None, port = None):
        '''
        Connects this instance with the instance sshhost over SSH.
        username is the user and pwd is the password.
        Port is the port number to connect to.
        See SSHClient.connect for more information on optional parameters
        that can be set when using the underlying layer instead of this one.
        '''
        if sshhost is None:
            sshhost = self.sshhost
        if user is None:
            user = self.username
        if pwd is None:
            pwd = self.pwd
        if port is not None:
            self.client.connect(sshhost, username = user, password = pwd, port=port)#(, timeout = 60)
        else:
            self.client.connect(sshhost, username = user, password = pwd)
        time.sleep(1)


    def run(self, command):
        '''
        Runs a command over SSH on the client.
        command is the command to execute.
        Returns the stdin, stdout, and stderr of the executing command, as a 3-tuple.
        '''
        return self.client.exec_command(command)

    def close_connection(self):
        '''
        Closes the SSH connection between this and the client.
        '''
        self.client.close()
