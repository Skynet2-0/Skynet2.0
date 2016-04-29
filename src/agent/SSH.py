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
        #self.client = SSHClient()
        
        
    def run(self, command):
        pass