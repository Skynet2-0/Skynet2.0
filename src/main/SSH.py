'''
Created on Apr 19, 2016

@author: Niels
'''
from pip._vendor.distlib._backport.tarfile import pwd

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
        
        
    def run(self, command):
        pass