'''
Created on Apr 29, 2016

@author: Stefan
'''
import unittest
from src.agent.SSH import *
from socket import socket
from threading import Thread


class SSHTest(unittest.TestCase):

    class Server(Thread):
        '''
        Plays the server for the connections.
        '''
        def __init__(self, hostname, port):
            super(SSHTest.Server, self).__init__()
            #super(Thread, self)
            self.server = socket()
            self.server.bind((hostname, port))
            self.server.listen(1)

        def run(self):
            self.server.accept()


    def setUp(self):
        port = 1050
        hostname = 'localhost'
        self.server = SSHTest.Server(hostname, port)
        self.server.deamon = False
        self.server.start()
        self.that = SSH(hostname, None, None, port)

    def tearDown(self):
        self.that.close_connection()
        self.server.close()
        self.server.join()

    def testNoError():
        (_, out, _) = self.that.run('ls')
        self.assertNotNone(out)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
