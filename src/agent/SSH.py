'''
Created on Apr 19, 2016

@author: Niels
'''
from paramiko.client import *

class SSH(object):
    '''
    This class enables the execution of SSH commands on a child server
    '''

    def __init__(self, ip, username, pwd):
        '''
        Constructor
        '''
        self.ip = ip
        self.username = username
        self.pwd = pwd
        self.client = SSHClient()
        self.client.load_system_host_keys()
        self.connect(self.ip)

    def connect(self, sshhost, user = None, pwd = None):
        '''
        Connects this instance with the instance sshhost over SSH.
        username is the user and pwd is the password.
        See SSHClient.connect for more information on optional parameters
        that can be set when using the underlying layer instead of this one.
        '''
        self.client.connect(sshhost, username = user, password = pwd)


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
