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

    def connect(self, sshhost, user = self.username, pwd = self.pwd):
        '''
        Connects this instance with the instance sshhost over SSH.
        username is the user and pwd is the password.
        See SSHClient.connect for more information on optional parameters
        that can be set when using the underlying layer instead of this one.
        '''
        self.client.connect(sshaddress, username = user, password = pwd)


    def run(self, command):
        pass
